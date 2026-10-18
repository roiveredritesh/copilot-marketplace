"""The SessionStart Haiku-window check must stay silent when Haiku compacts at <= 100K and speak otherwise.
No model calls, free to run.  usage: python evals/haiku_window_test.py"""
import json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(ROOT, "plugins", "core", "hooks", "haiku-window.sh")
OK = {"modelSettings": {"haiku": {"autoCompactWindow": 100000}}}

# (name, user settings, project settings, extra env, expect a note)
CASES = [
    ("no settings at all", None, None, {}, True),
    ("alias key at 100000", OK, None, {}, False),
    ("full model id at 100000", {"modelSettings": {"claude-haiku-5-5": {"autoCompactWindow": 100000}}}, None, {}, False),
    ("haiku window above 100K", {"modelSettings": {"haiku": {"autoCompactWindow": 200000}}}, None, {}, True),
    ("haiku window 'auto'", {"modelSettings": {"haiku": {"autoCompactWindow": "auto"}}}, None, {}, True),
    ("only another model set", {"modelSettings": {"claude-sonnet-5-5": {"autoCompactWindow": 100000}}}, None, {}, True),
    ("effort-only haiku entry", {"modelSettings": {"haiku": {"effortLevel": "low"}}}, None, {}, True),
    ("top-level window 100000", {"autoCompactWindow": 100000}, None, {}, False),
    ("project overrides user upward", OK, {"modelSettings": {"haiku": {"autoCompactWindow": 500000}}}, {}, True),
    ("set in project settings only", None, OK, {}, False),
    ("env window overrides per-model", OK, None, {"CLAUDE_CODE_AUTO_COMPACT_WINDOW": "200000"}, True),
    ("env window at 100000", None, None, {"CLAUDE_CODE_AUTO_COMPACT_WINDOW": "100000"}, False),
    ("opt-out", None, None, {"CLAUDE_CORE_HAIKU_CHECK": "0"}, False),
    ("malformed user settings", "{not json", None, {}, True),
]


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(data if isinstance(data, str) else json.dumps(data))


def main():
    failed = 0
    for name, user, project, extra, expect in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            cfg, proj = os.path.join(tmp, "cfg"), os.path.join(tmp, "proj")
            os.makedirs(proj)
            if user is not None:
                write(os.path.join(cfg, "settings.json"), user)
            if project is not None:
                write(os.path.join(proj, ".claude", "settings.json"), project)
            env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_CODE_AUTO_COMPACT_WINDOW", "CLAUDE_CORE_HAIKU_CHECK")}
            env.update(CLAUDE_CONFIG_DIR=cfg, CLAUDE_PROJECT_DIR=proj, **extra)
            r = subprocess.run(["bash", HOOK], capture_output=True, text=True, env=env, timeout=10)
            noted = "Cost note" in r.stdout
            ok = r.returncode == 0 and noted == expect and (noted or r.stdout == "")
            failed += not ok
            print(("ok    " if ok else "FAIL  ") + f"{name}: {'note' if noted else 'silent'}")
    print(f"\n{len(CASES) - failed}/{len(CASES)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
