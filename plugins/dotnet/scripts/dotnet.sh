#!/usr/bin/env bash
# Detect, build, or test any .NET repo (SDK-style or legacy .NET Framework) with condensed output.
# Usage: dotnet.sh detect|build|test|coverage|audit [solution-or-project]
# Env: DOTNET_TEST_FILTER (test/coverage filter expression), DOTNET_COVERAGE_FILE_REGEX (focus coverage on matching files)
# Always exits 0 and prints "STATUS: ..." first so callers parse text, not exit codes.
set -u
cmd=${1:-detect}; target=${2:-}
max=${DOTNET_SH_MAX_LINES:-40}
filter=${DOTNET_TEST_FILTER:-}

# Tracked + untracked files when inside git (skips ignored bin/obj); else find. Arg: filename regex.
list() {
  if git rev-parse --git-dir >/dev/null 2>&1; then git ls-files -co --exclude-standard
  else find . -type d \( -name bin -o -name obj -o -name node_modules -o -name .git \) -prune -o -type f -print | sed 's#^\./##'; fi | grep -E "$1"
}

projects=$(list '\.(cs|vb|fs)proj$')
[ -z "$projects" ] && { echo "STATUS: BLOCKED no .csproj/.vbproj/.fsproj found"; exit 0; }

if [ -z "$target" ]; then
  target=$(list '\.slnx$' | head -1)
  [ -z "$target" ] && target=$(list '\.sln$' | head -1)
  [ -z "$target" ] && [ "$(echo "$projects" | wc -l)" -eq 1 ] && target=$projects
  [ -z "$target" ] && { echo "STATUS: BLOCKED several projects and no solution; pass one as argument"; echo "$projects" | head -20; exit 0; }
fi

legacy=$(echo "$projects" | while IFS= read -r p; do grep -qE '<Project[^>]*Sdk=|<Sdk ' "$p" || echo "$p"; done)
tests=$(echo "$projects" | while IFS= read -r p; do grep -qiE 'xunit|nunit|MSTest|Microsoft\.NET\.Test\.Sdk' "$p" && echo "$p"; done)
tfms=$(echo "$projects" | while IFS= read -r p; do grep -ohE '<TargetFrameworks?>[^<]+|<TargetFrameworkVersion>[^<]+' "$p"; done | sed 's/.*>//' | tr ';' '\n' | sort -u | tr '\n' ' ')
windows=no; case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) windows=yes;; esac

vs_path() {
  local vswhere; vswhere="$(printenv 'ProgramFiles(x86)' || echo 'C:\Program Files (x86)')\Microsoft Visual Studio\Installer\vswhere.exe"
  [ -f "$vswhere" ] || return 1
  "$vswhere" -latest -products '*' -property installationPath | tr -d '\r'
}

# Keep error/failure lines, strip "[project]" suffixes and repo-absolute prefixes, dedupe, cap.
condense() { root=$(pwd -W 2>/dev/null || pwd); tr '\\' '/' | sed -E 's/ \[[^]]*\]$//' | sed "s#$root/##Ig" | grep -E "$1" | awk '!seen[$0]++' | head -n "$max"; }

case "$cmd" in
detect)
  echo "STATUS: OK"
  echo "entry: $target"
  echo "projects: $(echo "$projects" | wc -l) (legacy non-SDK: $(echo "$legacy" | grep -c .))"
  echo "frameworks: ${tfms:-unknown}"
  echo "test projects: $(echo "$tests" | grep -c .)"
  [ -n "$legacy" ] && echo "toolchain: msbuild (legacy projects present)$([ "$windows" = no ] && echo ' - NOT BUILDABLE on this OS')" || echo "toolchain: dotnet"
  list '(^|/)packages\.config$' | grep -q . && echo "packages.config: yes (restore via msbuild -p:RestorePackagesConfig=true)"
  list '(^|/)global\.json$' | grep -q . && echo "global.json: $(grep -oE '"version"[^,}]+' "$(list '(^|/)global\.json$' | head -1)") | installed: $(dotnet --list-sdks 2>/dev/null | cut -d' ' -f1 | tr '\n' ' ')"
  ;;
build|test)
  if [ -n "$legacy" ]; then
    [ "$windows" = no ] && { echo "STATUS: BLOCKED legacy .NET Framework projects need Windows + Visual Studio Build Tools"; exit 0; }
    vs=$(vs_path) || { echo "STATUS: BLOCKED vswhere not found; install Visual Studio Build Tools"; exit 0; }
    msbuild="$vs/MSBuild/Current/Bin/MSBuild.exe"
    out=$("$msbuild" "$target" -restore -p:RestorePackagesConfig=true -m -nologo -v:q -clp:ErrorsOnly 2>&1); rc=$?
  else
    out=$(dotnet build "$target" -nologo -v q -clp:'ErrorsOnly;NoSummary' 2>&1); rc=$?
  fi
  if [ $rc -ne 0 ]; then
    echo "STATUS: BUILD FAILED ($(echo "$out" | grep -cE ': error ') error lines)"
    echo "$out" | condense ': error |error MSB|error NU' ; exit 0
  fi
  [ "$cmd" = build ] && { echo "STATUS: BUILD OK"; exit 0; }
  [ -z "$tests" ] && { echo "STATUS: BUILD OK, no test projects"; exit 0; }
  if [ -n "$legacy" ]; then
    vstest="$vs/Common7/IDE/Extensions/TestPlatform/vstest.console.exe"
    dlls=$(echo "$tests" | while IFS= read -r p; do n=$(grep -oE '<AssemblyName>[^<]+' "$p" | sed 's/.*>//'); n=${n:-$(basename "${p%.*}")}
      find "$(dirname "$p")/bin" -name "$n.dll" -newer "$p" 2>/dev/null | head -1; done)
    [ -z "$dlls" ] && { echo "STATUS: BLOCKED test assemblies not found under bin/"; exit 0; }
    out=$(echo "$dlls" | tr '\n' '\0' | xargs -0 "$vstest" /Logger:console\;verbosity=minimal ${filter:+"/TestCaseFilter:$filter"} 2>&1); rc=$?
  else
    out=$(dotnet test "$target" --no-build -nologo -v q --logger 'console;verbosity=minimal' ${filter:+--filter "$filter"} 2>&1); rc=$?
  fi
  echo "$out" | grep -qiE 'No test matches|No test is available' && { echo "STATUS: NO TESTS MATCHED${filter:+ (filter: $filter)}"; exit 0; }
  summary=$(echo "$out" | grep -E 'Passed!|Failed!|Total tests|Passed:|Failed:' | tail -3)
  if [ $rc -ne 0 ]; then echo "STATUS: TESTS FAILED"; echo "$summary"; echo "$out" | condense '^\s*(Failed |Assert|Expected|Actual|at .* in .*:line|error )'
  else echo "STATUS: TESTS PASSED"; echo "$summary"; fi
  ;;
coverage)
  [ -n "$legacy" ] && { echo "STATUS: BLOCKED coverage needs SDK-style test projects (coverlet); legacy projects present"; exit 0; }
  dir=$(mktemp -d)
  out=$(dotnet test "$target" -nologo -v q --collect:"XPlat Code Coverage" --results-directory "$dir" ${filter:+--filter "$filter"} 2>&1); rc=$?
  files=$(find "$dir" -name 'coverage.cobertura.xml')
  [ -z "$files" ] && { echo "STATUS: BLOCKED no coverage file; add the coverlet.collector package to the test projects"; echo "$out" | condense ': error |Failed '; rm -rf "$dir"; exit 0; }
  [ $rc -ne 0 ] && echo "STATUS: COVERAGE (TESTS FAILED - numbers incomplete)" || echo "STATUS: COVERAGE"
  for f in $files; do echo "overall line-rate: $(grep -oE '<coverage [^>]*line-rate="[0-9.]+"' "$f" | grep -oE '[0-9.]+"$' | tr -d '"' | head -1)"; done
  # ponytail: strips paths up to the repo folder name; wrong only if a subfolder repeats that name
  echo "lowest classes (line-rate class file):"
  cat $files | grep -oE '<class name="[^"]+" filename="[^"]+" line-rate="[0-9.]+"' | tr '\\' '/' | sed "s#filename=\"[^\"]*/$(basename "$PWD")/#filename=\"#" | sed -E 's/<class name="([^"]+)" filename="([^"]+)" line-rate="([0-9.]+)"/\3 \1 \2/' | grep -E "${DOTNET_COVERAGE_FILE_REGEX:-.}" | sort -n | awk '!seen[$2]++' | head -n 15
  rm -rf "$dir"
  ;;
audit)
  echo "STATUS: AUDIT"
  if [ -n "$legacy" ] || list '(^|/)packages\.config$' | grep -q .; then echo "note: packages.config/legacy projects are not covered by 'dotnet list package' - migrate them to PackageReference"; fi
  if [ "$(echo "$legacy" | grep -c .)" -lt "$(echo "$projects" | grep -c .)" ]; then
    dotnet restore "$target" -v q >/dev/null 2>&1
    for kind in vulnerable deprecated outdated; do
      extra=; [ $kind = vulnerable ] && extra=--include-transitive
      rows=$(dotnet list "$target" package --$kind $extra 2>&1 | grep -E '^\s+> ' | sed -E 's/^\s+> //; s/\s+/ /g' | awk '!seen[$0]++')
      echo "$kind: $(echo "$rows" | grep -c .)"; echo "$rows" | grep . | head -n 20 | sed 's/^/  /'
    done
  fi
  echo "frameworks: ${tfms:-unknown}"
  # Report locations only, never the secret values.
  pat='(Password|Pwd)=[^;"'"'"' ]{3,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|xox[baprs]-[A-Za-z0-9-]{10,}|AccountKey=[A-Za-z0-9+/=]{20,}|sk-[A-Za-z0-9_-]{20,}'
  hits=$(git grep -nIE "$pat" -- . ':!*.md' 2>/dev/null | cut -d: -f1,2)
  echo "possible secrets: $(echo "$hits" | grep -c .)"; echo "$hits" | grep . | head -n 20 | sed 's/^/  /'
  ;;
*) echo "STATUS: BLOCKED unknown command '$cmd' (use detect|build|test|coverage|audit)";;
esac
exit 0
