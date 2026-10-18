"""SessionStart check: Haiku 5.5 prompts over 100K tokens bill at 5x, and Claude Code lets Haiku run to ~967K
before compacting unless a per-model window is set. Silent when `modelSettings.haiku.autoCompactWindow`
(or a claude-haiku-* entry) is at most 100000 in the effective settings: user, project, local, the claude process's
--settings, managed-settings files and cached server-managed settings. Otherwise prints one note. Never fails the session."""
import glob, json, os, re, subprocess, sys

LIMIT = 100000
MANAGED_DIRS = {"darwin": "/Library/Application Support/ClaudeCode", "win32": r"C:\Program Files\ClaudeCode"}


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def parse_settings_arg(value, cwd):
    """A --settings value: inline JSON or a path to a JSON file."""
    value = value.strip()
    if value.startswith("{"):
        try:
            return json.loads(value)
        except ValueError:
            return {}
    return load(value if os.path.isabs(value) else os.path.join(cwd, value))


def ancestor_args():
    """argv of each ancestor process, nearest first: exact from /proc (Linux, WSL), best-effort from ps (macOS)."""
    out, pid = [], os.getppid()
    for _ in range(10):
        if pid <= 1:
            break
        try:
            with open(f"/proc/{pid}/cmdline", "rb") as f:
                args = [a.decode("utf-8", "replace") for a in f.read().split(b"\0") if a]
            with open(f"/proc/{pid}/stat", encoding="utf-8") as f:
                ppid = int(f.read().rsplit(")", 1)[1].split()[1])
        except (OSError, ValueError, IndexError):
            try:
                line = subprocess.run(["ps", "-ww", "-o", "ppid=", "-o", "args=", "-p", str(pid)], capture_output=True,
                                      text=True, timeout=2).stdout.strip()
                ppid, _, cmd = line.partition(" ")
                ppid, args = int(ppid), [cmd]  # one string: split below
            except (OSError, ValueError, subprocess.SubprocessError):
                break
        out.append(args)
        pid = ppid
    return out


def is_claude(args):
    """The claude CLI itself: its binary, or node running its cli.js."""
    head = args[0].split()[:2] if len(args) == 1 else args[:2]
    return any(os.path.basename(a).lower() in ("claude", "claude.exe") or
               ("claude" in a.lower() and a.endswith((".js", ".mjs"))) for a in head)


def cli_settings():
    """The --settings of the nearest claude process (the session this hook belongs to), or {}."""
    for args in ancestor_args():
        found = None
        if len(args) == 1:  # ps: argv joined by spaces; inline JSON keeps its braces and quotes
            m = re.search(r"--settings[ =](\{.*\}|\S+)", args[0])
            found = m and m.group(1)
        else:
            for i, a in enumerate(args):
                if a == "--settings" and i + 1 < len(args):
                    found = args[i + 1]
                elif a.startswith("--settings="):
                    found = a.split("=", 1)[1]
        if found:
            return parse_settings_arg(found, os.getcwd())
        if is_claude(args):  # an outer claude's --settings belong to another session
            break
    return {}


def managed_settings():
    """managed-settings.json then managed-settings.d/*.json (alphabetical), merged; MDM and registry are not read."""
    d = os.environ.get("CLAUDE_CORE_MANAGED_SETTINGS_DIR") or MANAGED_DIRS.get(sys.platform, "/etc/claude-code")
    merged = {}
    for path in [os.path.join(d, "managed-settings.json")] + sorted(glob.glob(os.path.join(d, "managed-settings.d", "*.json"))):
        if os.path.basename(path).startswith("."):
            continue
        s = load(path)
        for k, v in s.items():
            merged[k] = dict(merged.get(k) or {}, **v) if isinstance(v, dict) and isinstance(merged.get(k), dict) else v
    return merged


def problem(env, files):
    """files: settings dicts from lowest to highest precedence (user, project, local, --settings, managed)."""
    raw = env.get("CLAUDE_CODE_AUTO_COMPACT_WINDOW", "").strip()
    if raw:  # overrides every per-model window, for every model
        return None if raw.isdigit() and int(raw) <= LIMIT else f"CLAUDE_CODE_AUTO_COMPACT_WINDOW={raw} overrides the Haiku window for every model"
    haiku, default = None, None
    for s in files:
        if isinstance(s.get("autoCompactWindow"), int):
            default = s["autoCompactWindow"]
        for model, cfg in (s.get("modelSettings") or {}).items():
            if (model == "haiku" or model.startswith("claude-haiku")) and isinstance(cfg, dict) and "autoCompactWindow" in cfg:
                haiku = cfg["autoCompactWindow"]
    window = haiku if haiku is not None else default
    if isinstance(window, int) and window <= LIMIT:
        return None
    return f"the Haiku auto-compact window is {window or 'not set'}"


# text only our templates have, and a line only the current versions have (see templates/)
TEMPLATES = {"Explore.md": "You are a read-only codebase search agent", "publisher.md": "You execute WORK ORDERS literally"}
CURRENT = "context budget"


def home_dir():
    return os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")


def check():
    """The Haiku window problem for this session's settings, or None."""
    home, proj = home_dir(), os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    files = [load(os.path.join(home, "settings.json")),
             load(os.path.join(proj, ".claude", "settings.json")),
             load(os.path.join(proj, ".claude", "settings.local.json")),
             cli_settings(),
             managed_settings(),
             load(os.path.join(home, "remote-settings.json"))]  # server-managed settings, cached locally
    return problem(os.environ, files)


def stale_templates():
    """User-level agents installed by an older /core:setup (ours by their text, but without the current rules)."""
    out = []
    for name, ours in TEMPLATES.items():
        try:
            with open(os.path.join(home_dir(), "agents", name), encoding="utf-8") as f:
                text = f.read()
        except OSError:
            continue
        if ours in text and CURRENT not in text:
            out.append(name)
    return out


def main():
    if os.environ.get("CLAUDE_CORE_HAIKU_CHECK", "1") == "0":
        return
    stale = stale_templates()
    if stale:
        print(f"Setup note (core plugin), worth one line to the user: ~/.claude/agents/{', '.join(stale)} came from "
              f"an older /core:setup and lacks the context-budget rule. Re-running /core:setup updates it.")
    p = check()
    if p:
        print(f"Cost note (core plugin), worth one line to the user: {p}, so Haiku sessions and subagents can grow "
              f"past 100K tokens, where Haiku 5.5 bills 5x. /core:setup sets modelSettings.haiku.autoCompactWindow "
              f"to 100000 (Haiku only). CLAUDE_CORE_HAIKU_CHECK=0 silences this note.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
