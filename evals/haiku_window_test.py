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
            env.update(CLAUDE_CONFIG_DIR=cfg, CLAUDE_PROJECT_DIR=proj, CLAUDE_CORE_MANAGED_SETTINGS_DIR=os.path.join(tmp, "managed"), **extra)
            r = subprocess.run(["bash", HOOK], capture_output=True, text=True, env=env, timeout=10)
            noted = "Cost note" in r.stdout
            ok = r.returncode == 0 and noted == expect and (noted or r.stdout == "")
            failed += not ok
            print(("ok    " if ok else "FAIL  ") + f"{name}: {'note' if noted else 'silent'}")
    # an Explore/publisher installed by an older /core:setup is flagged; the current templates and the user's own are not
    tpl = os.path.join(ROOT, "plugins", "core", "templates")
    old = "---\nname: Explore\nmodel: haiku\n---\nYou are a read-only codebase search agent. Find it.\n"
    for name, body, expect in [("older template", old, True), ("current template", open(os.path.join(tpl, "Explore.md")).read(), False),
                               ("user's own Explore", "---\nname: Explore\n---\nMy own agent.\n", False)]:
        with tempfile.TemporaryDirectory() as tmp:
            write(os.path.join(tmp, "agents", "Explore.md"), body)
            write(os.path.join(tmp, "settings.json"), OK)
            env = dict(os.environ, CLAUDE_CONFIG_DIR=tmp, CLAUDE_PROJECT_DIR=tmp, CLAUDE_CORE_MANAGED_SETTINGS_DIR=os.path.join(tmp, "m"))
            env.pop("CLAUDE_CODE_AUTO_COMPACT_WINDOW", None)
            out = subprocess.run(["bash", HOOK], capture_output=True, text=True, env=env, timeout=10).stdout
            ok = ("Setup note" in out) == expect and "Cost note" not in out
            failed += not ok
            CASES.append(name)
            print(("ok    " if ok else "FAIL  ") + f"{name}: {'note' if 'Setup note' in out else 'silent'}")
    # settings beyond the three files: the claude process's --settings, managed settings, cached server-managed settings
    BIG = {"modelSettings": {"haiku": {"autoCompactWindow": 500000}}}
    for name, setup, expect in [
        ("--settings inline JSON", lambda t: (["--settings", json.dumps(OK)], {}), False),
        ("--settings file path", lambda t: (write(os.path.join(t, "s.json"), OK) or ["--settings", os.path.join(t, "s.json")], {}), False),
        ("--settings=inline form", lambda t: (["--settings=" + json.dumps(OK)], {}), False),
        ("--settings beyond the nearest claude ignored", lambda t: (["claude", "--settings", json.dumps(OK)], {"inner_claude": True}), True),
        ("managed-settings.json", lambda t: (write(os.path.join(t, "managed", "managed-settings.json"), OK) or [], {}), False),
        ("managed-settings.d drop-in", lambda t: (write(os.path.join(t, "managed", "managed-settings.d", "20-haiku.json"), OK) or [], {}), False),
        ("managed raises the window above user", lambda t: (write(os.path.join(t, "cfg", "settings.json"), OK) or
                                                            write(os.path.join(t, "managed", "managed-settings.json"), BIG) or [], {}), True),
        ("server-managed (remote-settings.json)", lambda t: (write(os.path.join(t, "cfg", "remote-settings.json"), OK) or [], {}), False),
    ]:
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "cfg"), exist_ok=True)
            args, opt = setup(tmp)
            env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_CODE_AUTO_COMPACT_WINDOW", "CLAUDE_CORE_HAIKU_CHECK")}
            env.update(CLAUDE_CONFIG_DIR=os.path.join(tmp, "cfg"), CLAUDE_PROJECT_DIR=tmp, CLAUDE_CORE_MANAGED_SETTINGS_DIR=os.path.join(tmp, "managed"))
            run = ["bash", HOOK]
            if opt.get("inner_claude"):  # outer process with --settings, then a nested `claude` process without them
                inner = os.path.join(tmp, "claude")
                write(inner, '#!/usr/bin/env bash\nbash "$HOOK"\n')
                os.chmod(inner, 0o755)
                env["HOOK"] = HOOK
                run = [sys.executable, "-c", f"import subprocess; subprocess.run([{inner!r}])", "--settings", json.dumps(OK)]
            elif args:  # a parent process whose argv carries --settings, like `claude --settings ...`
                run = [sys.executable, "-c", f"import subprocess; subprocess.run(['bash', {HOOK!r}])"] + args
            out = subprocess.run(run, capture_output=True, text=True, env=env, timeout=10).stdout
            ok = ("Cost note" in out) == expect
            failed += not ok
            CASES.append(name)
            print(("ok    " if ok else "FAIL  ") + f"{name}: {'note' if 'Cost note' in out else 'silent'}")
    print(f"\n{len(CASES) - failed}/{len(CASES)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
