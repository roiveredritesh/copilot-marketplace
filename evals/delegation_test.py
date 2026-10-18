"""The SessionStart delegation policy must name only agents that exist, stay small, and honor the opt-out.
No model calls, free to run.  usage: python evals/delegation_test.py"""
import glob, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, "plugins", "core")
HOOK = os.path.join(CORE, "hooks", "delegation.sh")
MAX_CHARS = 1600  # ~400 tokens, paid (cached) on every request of every session


def run(env_extra):
    env = dict(os.environ, **env_extra)
    return subprocess.run(["bash", HOOK], capture_output=True, text=True, env=env, timeout=10)


def main():
    failed = []
    agents = {os.path.basename(p)[:-3] for p in glob.glob(os.path.join(CORE, "agents", "*.md"))}
    on = run({})
    named = set(re.findall(r"\bcore:([a-z-]+)", on.stdout))
    checks = [
        ("exits 0", on.returncode == 0),
        ("prints the policy", "Delegation policy" in on.stdout),
        (f"names only existing agents {sorted(named - agents)}", named and named <= agents),
        (f"names scout and runner", {"scout", "runner"} <= named),
        (f"at most {MAX_CHARS} chars (is {len(on.stdout)})", len(on.stdout) <= MAX_CHARS),
        ("CLAUDE_CORE_DELEGATION=0 prints nothing", run({"CLAUDE_CORE_DELEGATION": "0"}).stdout == ""),
    ]
    for name, ok in checks:
        print(("ok    " if ok else "FAIL  ") + name)
        if not ok:
            failed.append(name)
    for a in sorted(agents):
        text = open(os.path.join(CORE, "agents", a + ".md"), encoding="utf-8").read()
        ok = re.search(r"^description: Use proactively", text, re.M) is not None
        print(("ok    " if ok else "FAIL  ") + f"agents/{a}.md description starts with 'Use proactively'")
        if not ok:
            failed.append(a)
    print(f"\n{len(failed)} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
