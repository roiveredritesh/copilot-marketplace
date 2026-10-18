"""SessionStart check: Haiku 5.5 prompts over 100K tokens bill at 5x, and Claude Code lets Haiku run to ~967K
before compacting unless a per-model window is set. Silent when `modelSettings.haiku.autoCompactWindow`
(or a claude-haiku-* entry) is at most 100000; otherwise prints one note. Never fails the session."""
import json, os, sys

LIMIT = 100000


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def problem(env, files):
    """files: settings dicts from lowest to highest precedence (user, project, local)."""
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


def main():
    if os.environ.get("CLAUDE_CORE_HAIKU_CHECK", "1") == "0":
        return
    home = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")
    proj = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    files = [load(os.path.join(home, "settings.json")),
             load(os.path.join(proj, ".claude", "settings.json")),
             load(os.path.join(proj, ".claude", "settings.local.json"))]
    p = problem(os.environ, files)
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
