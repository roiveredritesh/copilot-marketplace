"""Keep Haiku inside its 100K price tier without losing its place.

PreToolUse, Haiku subagents (scout, runner, publisher, Explore...): project the next prompt (last request
size + this call's estimated result). Over the work-order budget (default 60K, below the ~72K compaction
point), deny the call and have the agent return now with `not done:`. It never compacts, so it can't lose
its place, and no request crosses 100K.
PreToolUse, Haiku subagents with a maxTurns: on the next-to-last turn, tell the agent its next reply must be
the answer, so hitting the limit returns results instead of nothing.
PreToolUse, Haiku main session with the 100K window set: compaction stays the safety net, but a call whose result
would push the prompt past 95K before compaction runs is denied with a way to make it smaller: a Read gets a line
range that fits, Bash a `| head`, an MCP or other tool a subagent that returns only what is needed.
SessionStart (compact), Haiku main session: re-inject the user's request and the tool calls already made.

PreToolUse, every model: a Read with offset 0 is rewritten to offset 1 (Read numbers from 0 otherwise).

Any error, a non-Haiku model, or CLAUDE_CORE_HAIKU_GUARD=0 means allow and print nothing (except the offset fix)."""
import json, os, re, sys

BUDGET = int(os.environ.get("CLAUDE_CORE_HAIKU_BUDGET") or 60000)  # subagents: stop before compaction
MAIN_LIMIT = 95000  # main session: what a prompt may reach before compaction runs
READ_MAX = 25000  # Read refuses bigger results, so a result never exceeds this
CHARS_PER_TOKEN = 1.9  # Haiku 5.5, measured: shell 1.9, Markdown 2.4, Python 2.6 (with Read line prefixes)
# Bash/PowerShell: ~30K chars come back inline, larger output is saved to a file behind a ~2K preview
ESTIMATE = {"Bash": 16000, "PowerShell": 16000, "Grep": 4000, "Glob": 1500, "WebFetch": 4000, "WebSearch": 3000,
            "Agent": 3000, "Edit": 1500, "Write": 500, "TodoWrite": 300, "AskUserQuestion": 500}
LINE_TOKENS = 60  # per line of a `| head -n N` command's output
IMAGE = 1600  # tokens per image block; its base64 in the transcript says nothing about its cost
TAIL, QUICK = 4 << 20, 256 << 10  # PreToolUse reads QUICK first: most calls only need the model check


def entries(path, tail=TAIL):
    """JSON lines of a transcript; only the last `tail` bytes when the file is large."""
    with open(path, "rb") as f:
        f.seek(0, 2)
        size = f.tell()
        f.seek(max(0, size - tail))
        data = f.read().decode("utf-8", "replace").splitlines()
    if size > tail:
        data = data[1:]  # first line is cut
    out = []
    for line in data:
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def last_request(rows):
    """(model, prompt tokens, tool_use blocks, index) of the latest assistant message with usage."""
    for i in range(len(rows) - 1, -1, -1):
        m = rows[i].get("message") or {}
        if rows[i].get("type") == "assistant" and m.get("usage"):
            u, mid = m["usage"], m.get("id")
            size = u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
            uses = [b for r in rows if r.get("type") == "assistant" and (r.get("message") or {}).get("id") == mid
                    for b in (r["message"].get("content") or []) if isinstance(b, dict) and b.get("type") == "tool_use"]
            return m.get("model") or "", size, uses, i
    return "", 0, [], -1


def result_tokens(content):
    if isinstance(content, str):
        return int(len(content) / CHARS_PER_TOKEN)
    total = 0
    for b in content if isinstance(content, list) else []:
        if isinstance(b, dict) and b.get("type") == "image":
            total += IMAGE
        elif isinstance(b, dict):
            total += int(len(b.get("text") or json.dumps(b)) / CHARS_PER_TOKEN)
    return total


def results_since(rows, i):
    """Estimated tokens of the tool results written after row i (the transcript can lag the hook)."""
    return sum(result_tokens(b.get("content")) for r in rows[i + 1:] if r.get("type") == "user"
               for b in ((r.get("message") or {}).get("content") or []) if isinstance(b, dict) and b.get("type") == "tool_result")


def max_turns(agent_type, cwd):
    """maxTurns from the agent's file: core:<name> in this plugin, <name> in the project or user agents dir."""
    plugin, _, name = agent_type.rpartition(":")
    root = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    home = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")
    paths = [os.path.join(root, "agents", name + ".md")] if plugin == "core" else \
            [] if plugin else [os.path.join(cwd, ".claude", "agents", name + ".md"), os.path.join(home, "agents", name + ".md")]
    for p in paths:
        try:
            with open(p, encoding="utf-8") as f:
                head = f.read(4096).split("\n---", 1)[0]
        except OSError:
            continue
        for line in head.splitlines():
            if line.startswith("maxTurns:") and line.split(":", 1)[1].strip().isdigit():
                return int(line.split(":", 1)[1])
        return None
    return None


def window_set():
    """True when Haiku compacts at <= 100K (the haiku_window check finds no problem)."""
    try:
        sys.dont_write_bytecode = True  # no __pycache__ inside the installed plugin
        import haiku_window
        return haiku_window.check() is None
    except Exception:
        return False


def read_estimate(inp, cwd):
    """Tokens a Read result will take: the requested lines plus line-number prefixes."""
    path = inp.get("file_path") or ""
    path = path if os.path.isabs(path) else os.path.join(cwd, path)
    offset, limit = max(int(inp.get("offset") or 1), 1), int(inp.get("limit") or 2000)
    if os.path.splitext(path)[1].lower() in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
        return IMAGE, 0, IMAGE
    if os.path.splitext(path)[1].lower() in (".pdf", ".ipynb"):
        return READ_MAX, 0, READ_MAX
    chars, lines = 0, 0
    with open(path, "rb") as f:
        for n, line in enumerate(f, 1):
            if n >= offset + limit:
                break
            if n >= offset:
                chars, lines = chars + len(line) + 7, lines + 1
    raw = int(chars / CHARS_PER_TOKEN)
    return min(raw, READ_MAX), lines, raw


def estimate(use, cwd):
    if use.get("name") == "Read":
        try:
            return read_estimate(use.get("input") or {}, cwd)[0]
        except (OSError, ValueError, TypeError):
            return 2000
    if use.get("name") in ("Bash", "PowerShell"):  # a command bounded by head/tail is estimated from its line count
        m = re.search(r"\|\s*(?:head|tail|Select-Object\s+-(?:First|Last))\s+(?:-n\s*)?-?(\d+)\s*$", (use.get("input") or {}).get("command") or "")
        if m:
            return min(int(m.group(1)) * LINE_TOKENS, ESTIMATE["Bash"])
    if (use.get("name") or "").startswith("mcp__"):  # Claude Code caps an MCP result at MAX_MCP_OUTPUT_TOKENS
        return int(os.environ.get("MAX_MCP_OUTPUT_TOKENS") or 25000)
    return ESTIMATE.get(use.get("name"), 4000)


def deny(reason):
    return {"permissionDecision": "deny", "permissionDecisionReason": reason}


def pre_tool_use(hook):
    sub = hook.get("agent_id")
    path = hook.get("transcript_path") or ""
    if sub:
        path = os.path.join(os.path.splitext(path)[0], "subagents", f"agent-{sub}.jsonl")
    if not os.path.isfile(path):
        return
    rows = entries(path, QUICK)
    model, size, uses, at = last_request(rows)
    if at < 0:  # one huge row filled the quick tail
        rows = entries(path)
        model, size, uses, at = last_request(rows)
    if "haiku" not in model or not size:
        return
    if any(r.get("type") == "system" and r.get("subtype") == "compact_boundary" for r in rows[at + 1:]):
        return  # compacted since the last recorded request: the context was just reset
    cwd = hook.get("cwd") or os.getcwd()
    me = hook.get("tool_use_id")
    current = estimate({"name": hook.get("tool_name"), "input": hook.get("tool_input")}, cwd)
    current_written = any(u.get("id") == me for u in uses)
    if current_written:  # transcript is current: add this message's other calls
        projected = size + current + sum(estimate(u, cwd) for u in uses if u.get("id") != me)
    else:  # transcript lags: that message's calls already ran, their results are on disk
        projected = size + results_since(rows, at) + current
    log = os.environ.get("CLAUDE_CORE_HAIKU_GUARD_LOG")
    if log:
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps({"agent": hook.get("agent_type", "main"), "tool": hook.get("tool_name"), "last": size,
                                "current": current, "projected": projected, "lagging": not current_written}) + "\n")
    if sub and projected > BUDGET:
        return deny(f"Context budget: this work order has used ~{size // 1000}K tokens, and this call would bring the "
             f"prompt to ~{projected // 1000}K (budget {BUDGET // 1000}K, below Haiku's 100K price tier and before "
             f"compaction). Make no more tool calls. Return now in the work order's return format with what you "
             f"have found, then one line `not done: <the steps or files not finished>`.")
    elif sub:
        limit = max_turns(hook.get("agent_type") or "", cwd)
        turn = len({(r.get("message") or {}).get("id") for r in rows if r.get("type") == "assistant"
                    and (r.get("message") or {}).get("usage")}) + (0 if current_written else 1)
        if limit and turn >= limit - 1:
            return {"additionalContext":
                    f"Turn limit (core plugin turn counter): turn {turn} of this agent's maxTurns {limit} is done. "
                    f"The run is cut off after turn {limit}, so the next reply is the last one that reaches the caller."}
    elif projected > MAIN_LIMIT and size < MAIN_LIMIT - 10000 and hook.get("tool_name") != "Agent" and window_set():
        # size already past ~85K means compaction isn't running at ~80K: denying couldn't help, so allow
        tool = hook.get("tool_name") or ""
        if tool == "Read":
            try:
                est, lines, raw = read_estimate(hook.get("tool_input") or {}, cwd)
                room = max(MAIN_LIMIT - (projected - est), 2000)
                fit = max(int(lines * room / max(raw, 1)), 20)
            except (OSError, ValueError, TypeError):
                fit = 200
            how = f"Read a smaller range: at most {fit} lines from the same offset, then continue."
        elif tool in ("Bash", "PowerShell"):
            how = "Bound the output: end the command with `| head -n 100` (or write it to a file and Read a range), then continue."
        else:
            how = ("Make this call inside a subagent (Agent tool) that returns only the part you need, "
                   "or ask the user to run /compact first.")
        return deny(f"This call's result could bring the Haiku prompt to ~{projected // 1000}K tokens, past the 100K price "
             f"tier, before compaction can run. {how}")


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list) and not any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
        return "\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def describe(use):
    i, n = use.get("input") or {}, use.get("name")
    if n == "Read":
        rng = f" {i.get('offset', 1)}+{i['limit']}" if i.get("limit") else ""
        return f"Read {i.get('file_path', '')}{rng}"
    if n in ("Edit", "Write", "NotebookEdit"):
        return f"{n} {i.get('file_path') or i.get('notebook_path', '')}"
    if n in ("Bash", "PowerShell"):
        return f"{n} `{(i.get('command') or '')[:80]}`"
    if n in ("Grep", "Glob"):
        return f"{n} {i.get('pattern', '')} {i.get('path', '')}".strip()
    if n == "Agent":
        return f"Agent {i.get('subagent_type', '')}: {(i.get('description') or '')[:60]}"
    return n or "?"


def after_compact(hook):
    path = hook.get("transcript_path") or ""
    if not os.path.isfile(path):
        return
    rows = [r for r in entries(path) if not r.get("isSidechain")]
    model = last_request(rows)[0]
    if "haiku" not in model:
        return
    start, ask = None, ""
    for i in range(len(rows) - 1, -1, -1):
        r = rows[i]
        if r.get("type") != "user" or r.get("isMeta") or r.get("isCompactSummary"):
            continue
        t = text_of((r.get("message") or {}).get("content")).strip()
        if t and not t.startswith(("<system-reminder>", "<local-command", "Caveat:")):
            start, ask = i, t
            break
    if start is None:
        return
    calls = [describe(b) for r in rows[start + 1:] if r.get("type") == "assistant"
             for b in ((r.get("message") or {}).get("content") or []) if isinstance(b, dict) and b.get("type") == "tool_use"]
    if not calls:
        return
    shown = calls[-40:]
    more = f" ({len(calls) - len(shown)} earlier calls not listed)" if len(calls) > len(shown) else ""
    ask = ask if len(ask) <= 1500 else ask[:1500] + " [...]"
    print("Resume point after compaction (core plugin). The user's current request, verbatim:\n"
          f"<request>\n{ask}\n</request>\n"
          f"Tool calls already made for it, oldest first{more}:\n- " + "\n- ".join(shown) +
          "\nContinue from the first step not covered above. Results of these calls are in the summary, "
          "so don't repeat them.")


def zero_offset_fix(hook):
    """Read numbers lines from 0 when offset is 0, so every path:line cited from it is one too low. Any model."""
    inp = hook.get("tool_input") or {}
    if hook.get("tool_name") == "Read" and str(inp.get("offset", "")).strip() == "0":
        return {"updatedInput": dict(inp, offset=1)}  # no permissionDecision: permissions are decided as usual
    return {}


def main():
    hook = json.load(sys.stdin)
    event = hook.get("hook_event_name")
    guard = os.environ.get("CLAUDE_CORE_HAIKU_GUARD", "1") != "0"
    if event == "PreToolUse":
        out = (pre_tool_use(hook) if guard else None) or {}
        if out.get("permissionDecision") != "deny":
            out.update(zero_offset_fix(hook))
        if out:
            print(json.dumps({"hookSpecificOutput": dict({"hookEventName": "PreToolUse"}, **out)}))
    elif guard and event == "SessionStart" and hook.get("source") == "compact":
        after_compact(hook)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
