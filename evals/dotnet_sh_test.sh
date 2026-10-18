#!/usr/bin/env bash
# dotnet.sh status lines for restore and build outcomes, using a fake `dotnet` on PATH. No SDK or network needed.
# usage: bash evals/dotnet_sh_test.sh
root=$(cd "$(dirname "$0")/.." && pwd); script="$root/plugins/dotnet/scripts/dotnet.sh"
pass=0; fail=0
check() { if [[ "$2" == *"$3"* ]]; then pass=$((pass+1)); echo "ok    $1"; else fail=$((fail+1)); echo "FAIL  $1: got '$(echo "$2" | head -1)'"; fi; }
t=$(mktemp -d); trap 'rm -rf "$t"' EXIT
mkdir -p "$t/repo/src/App" "$t/bin"
printf '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net8.0</TargetFramework></PropertyGroup></Project>\n' > "$t/repo/src/App/App.csproj"
# fake dotnet: $FAKE_RESTORE / $FAKE_BUILD pick the outcome; it records the retry setting it was given
cat > "$t/bin/dotnet" <<'X'
#!/usr/bin/env bash
echo "$1 tries=$NUGET_ENHANCED_MAX_NETWORK_TRY_COUNT" >> "$FAKE_LOG"
case "$1" in
  restore) case "$FAKE_RESTORE" in
    unreachable) echo "src/App/App.csproj : error NU1301: Unable to load the service index for source https://api.nuget.org/v3/index.json."; exit 1;;
    conflict) echo "src/App/App.csproj : error NU1605: Detected package downgrade: Foo from 2.0.0 to 1.0.0."; exit 1;;
    *) exit 0;; esac;;
  list) case "$FAKE_LIST" in
    vulnerable-only-ok) [[ " $* " == *" --vulnerable "* ]] && { echo "   > Newtonsoft.Json   12.0.1   12.0.1   High"; exit 0; }
      echo "error: Unable to load the service index for source https://api.nuget.org/v3/index.json."; exit 1;;
    *) [[ " $* " == *" --vulnerable "* ]] && echo "   > Newtonsoft.Json   12.0.1   12.0.1   High"; exit 0;; esac;;
  build) [[ " $* " == *" --no-restore "* ]] || echo "BUILD WITHOUT --no-restore" >> "$FAKE_LOG"
    case "$FAKE_BUILD" in
    error) echo "src/App/Program.cs(3,10): error CS1002: ; expected [src/App/App.csproj]"; exit 1;;
    *) exit 0;; esac;;
esac
X
chmod +x "$t/bin/dotnet"
run() { (cd "$t/repo" && PATH="$t/bin:$PATH" FAKE_LOG="$t/log" FAKE_RESTORE="$1" FAKE_BUILD="$2" bash "$script" build); }
: > "$t/log"
check "unreachable feed is a restore failure, named" "$(run unreachable ok)" "STATUS: RESTORE FAILED (package source unreachable: https://api.nuget.org/v3/index.json)"
check "no build after a failed restore" "$(cat "$t/log")" "restore tries=2"
[[ "$(cat "$t/log")" == *build* ]] && { fail=$((fail+1)); echo "FAIL  build ran after a failed restore"; } || { pass=$((pass+1)); echo "ok    build skipped after a failed restore"; }
check "other restore errors are counted" "$(run conflict ok)" "STATUS: RESTORE FAILED (1 error lines)"
check "compile error is a build failure" "$(run ok error)" "STATUS: BUILD FAILED (1 error lines)"
check "clean build" "$(run ok ok)" "STATUS: BUILD OK"
[[ "$(cat "$t/log")" == *"BUILD WITHOUT --no-restore"* ]] && { fail=$((fail+1)); echo "FAIL  build restored again"; } || { pass=$((pass+1)); echo "ok    build uses --no-restore"; }
: > "$t/log"; (cd "$t/repo" && PATH="$t/bin:$PATH" FAKE_LOG="$t/log" NUGET_ENHANCED_MAX_NETWORK_TRY_COUNT=6 bash "$script" build >/dev/null)
check "a user's own retry setting wins" "$(cat "$t/log")" "restore tries=6"
audit() { (cd "$t/repo" && PATH="$t/bin:$PATH" FAKE_LOG="$t/log" FAKE_RESTORE="$1" FAKE_LIST="$2" bash "$script" audit); }
out=$(audit unreachable ok)
check "audit: unreachable feed is INCOMPLETE, not clean" "$out" "STATUS: AUDIT INCOMPLETE (not checked: vulnerable deprecated outdated)"
[[ "$out" == *"vulnerable: 0"* ]] && { fail=$((fail+1)); echo "FAIL  audit printed a clean 0 it never checked"; } || { pass=$((pass+1)); echo "ok    audit prints no unchecked 0"; }
out=$(audit ok ok)
check "audit: all checks ran" "$(echo "$out" | head -1)" "STATUS: AUDIT"
check "audit: vulnerable rows counted" "$out" "vulnerable: 1"
check "audit: one failing check makes it INCOMPLETE" "$(audit ok vulnerable-only-ok | head -1)" "STATUS: AUDIT INCOMPLETE (not checked: deprecated outdated)"
echo; echo "$pass/$((pass+fail)) passed"
[ "$fail" = 0 ]
