"""The Haiku context guard: executors stop before the budget, main-session reads stay under 100K, and a
compacted Haiku session gets its resume point. Synthetic transcripts, no model calls, free to run.
usage: python evals/haiku_guard_test.py"""
import json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(ROOT, "plugins", "core", "hooks", "haiku-guard.sh")


def assistant(mid, model, size, uses=()):
    content = [{"type": "tool_use", "id": i, "name": n, "input": inp} for i, n, inp in uses]
    return {"type": "assistant", "message": {"id": mid, "model": model, "content": content,
                                             "usage": {"input_tokens": 5, "cache_read_input_tokens": size - 5, "cache_creation_input_tokens": 0}}}


def user(text, **extra):
    return dict({"type": "user", "message": {"role": "user", "content": text}}, **extra)


def run(tmp, rows, hook, sub=None, env=None):
    main = os.path.join(tmp, "sess.jsonl")
    path = os.path.join(tmp, "sess", "subagents", f"agent-{sub}.jsonl") if sub else main
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("\n".join(json.dumps(r) for r in rows) + "\n")
    hook = dict(hook, transcript_path=main, cwd=tmp, **({"agent_id": sub, "agent_type": "core:scout"} if sub else {}))
    cfg = os.path.join(tmp, "cfg")  # the 100K Haiku window is set unless a case says otherwise
    os.makedirs(cfg, exist_ok=True)
    with open(os.path.join(cfg, "settings.json"), "w") as f:
        json.dump({"modelSettings": {"haiku": {"autoCompactWindow": 100000}}}, f)
    e = {k: v for k, v in os.environ.items() if not k.startswith("CLAUDE_CORE_HAIKU") and k != "CLAUDE_CODE_AUTO_COMPACT_WINDOW"}
    e.update(CLAUDE_CONFIG_DIR=cfg, CLAUDE_PROJECT_DIR=tmp, CLAUDE_CORE_MANAGED_SETTINGS_DIR=os.path.join(tmp, "managed"), **(env or {}))
    r = subprocess.run(["bash", HOOK], input=json.dumps(hook), capture_output=True, text=True, env=e, timeout=10)
    return r.returncode, r.stdout


def pre(tool, inp, tid="t9"):
    return {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": inp, "tool_use_id": tid}


def main():
    failed, n = 0, 0
    with tempfile.TemporaryDirectory() as tmp:
        big = os.path.join(tmp, "big.txt")  # 400 lines, ~40K chars -> ~22K tokens estimated
        small = os.path.join(tmp, "small.txt")  # 20 lines -> ~1K tokens
        with open(big, "w") as f:
            f.write("".join(f"{i:04d} " + "x" * 90 + "\n" for i in range(400)))
        with open(small, "w") as f:
            f.write("".join(f"line {i}\n" for i in range(20)))
        H, S = "claude-haiku-5-5", "claude-sonnet-5-5"
        read_big = ("t9", "Read", {"file_path": big})
        cases = [
            # name, rows, hook input, subagent id, env, expect substring ("" = silent)
            ("sub: small read under budget", [assistant("m1", H, 20000, [("t9", "Read", {"file_path": small})])], pre("Read", {"file_path": small}), "a1", None, ""),
            ("sub: big read over budget", [assistant("m1", H, 45000, [read_big])], pre("Read", {"file_path": big}), "a1", None, "not done:"),
            ("sub: already over budget, any tool", [assistant("m1", H, 61000, [("t9", "Grep", {"pattern": "x"})])], pre("Grep", {"pattern": "x"}), "a1", None, "Context budget"),
            ("sub: parallel reads add up", [assistant("m1", H, 40000, [("t1", "Read", {"file_path": big}), read_big])], pre("Read", {"file_path": big}), "a1", None, "Context budget"),
            ("sub: not Haiku", [assistant("m1", S, 90000, [read_big])], pre("Read", {"file_path": big}), "a1", None, ""),
            ("sub: budget raised by env", [assistant("m1", H, 45000, [read_big])], pre("Read", {"file_path": big}), "a1", {"CLAUDE_CORE_HAIKU_BUDGET": "90000"}, ""),
            ("sub: guard off", [assistant("m1", H, 61000, [read_big])], pre("Read", {"file_path": big}), "a1", {"CLAUDE_CORE_HAIKU_GUARD": "0"}, ""),
            ("main: read that crosses 95K", [assistant("m1", H, 78000, [read_big])], pre("Read", {"file_path": big}), None, None, "at most"),
            ("main: read that fits", [assistant("m1", H, 78000, [("t9", "Read", {"file_path": small})])], pre("Read", {"file_path": small}), None, None, ""),
            ("main: Bash is not limited", [assistant("m1", H, 90000, [("t9", "Bash", {"command": "ls"})])], pre("Bash", {"command": "ls"}), None, None, ""),
            ("main: not Haiku", [assistant("m1", S, 90000, [read_big])], pre("Read", {"file_path": big}), None, None, ""),
            ("missing transcript", [], pre("Read", {"file_path": big}), None, None, ""),
            # the main transcript can lag the hook: the current call's message isn't written yet
            ("main: lagging, results on disk counted", [assistant("m1", H, 60000, [("t1", "Read", {"file_path": big})]),
                                                        user([{"type": "tool_result", "tool_use_id": "t1", "content": "y" * 40000}])],
             pre("Read", {"file_path": big}), None, None, "at most"),
            ("main: lagging, small total allowed", [assistant("m1", H, 30000, [("t1", "Read", {"file_path": small})]),
                                                    user([{"type": "tool_result", "tool_use_id": "t1", "content": "y" * 2000}])],
             pre("Read", {"file_path": big}), None, None, ""),
            ("main: window not set, no read limit", [assistant("m1", H, 78000, [read_big])], pre("Read", {"file_path": big}), None,
             {"CLAUDE_CODE_AUTO_COMPACT_WINDOW": "1000000"}, ""),
            ("sub: image result counts as an image", [assistant("m1", H, 30000, [("t1", "Read", {"file_path": "x.png"})]),
                                                      user([{"type": "tool_result", "tool_use_id": "t1", "content": [
                                                          {"type": "image", "source": {"type": "base64", "data": "A" * 400000}}]}])],
             pre("Read", {"file_path": small}), "a1", None, ""),
            # scout has maxTurns 12: warn on turn 11 so turn 12 returns the results
            ("sub: turn 11 of 12 warns", [assistant(f"m{i}", H, 15000 + i, [(f"t{i}", "Read", {"file_path": small})]) for i in range(1, 11)]
             + [assistant("m11", H, 15100, [read_big[:2] + ({"file_path": small},)])], pre("Read", {"file_path": small}), "a1", None, "Turn limit"),
            ("sub: turn 10 of 12 silent", [assistant(f"m{i}", H, 15000 + i, [(f"t{i}", "Read", {"file_path": small})]) for i in range(1, 10)]
             + [assistant("m10", H, 15100, [read_big[:2] + ({"file_path": small},)])], pre("Read", {"file_path": small}), "a1", None, ""),
            # main session, other tools: each gets a remedy that can actually shrink its result
            ("main: MCP call near compaction", [assistant("m1", H, 72000, [("t9", "mcp__jira__getIssue", {"key": "A-1"})])],
             pre("mcp__jira__getIssue", {"key": "A-1"}), None, None, "subagent"),
            ("main: MCP call with room", [assistant("m1", H, 40000, [("t9", "mcp__jira__getIssue", {"key": "A-1"})])],
             pre("mcp__jira__getIssue", {"key": "A-1"}), None, None, ""),
            ("main: unbounded Bash near compaction", [assistant("m1", H, 82000, [("t9", "Bash", {"command": "git log"})])],
             pre("Bash", {"command": "git log"}), None, None, "head -n"),
            ("main: Bash bounded by head", [assistant("m1", H, 82000, [("t9", "Bash", {"command": "git log | head -n 100"})])],
             pre("Bash", {"command": "git log | head -n 100"}), None, None, ""),
            ("main: Agent is never denied", [assistant("m1", H, 84000, [("t9", "Agent", {"subagent_type": "core:scout"})])],
             pre("Agent", {"subagent_type": "core:scout"}), None, None, ""),
            ("main: past 85K, compaction not running", [assistant("m1", H, 88000, [read_big])], pre("Read", {"file_path": big}), None, None, ""),
            # Read numbers lines from 0 when offset is 0: rewritten to 1 for every model, never auto-approved
            ("offset 0 rewritten (any model)", [assistant("m1", S, 20000, [("t9", "Read", {"file_path": small, "offset": 0})])],
             pre("Read", {"file_path": small, "offset": 0, "limit": 5}), None, None, '"updatedInput"'),
            ("offset 0 rewritten with the guard off", [assistant("m1", S, 20000, [("t9", "Read", {"file_path": small, "offset": 0})])],
             pre("Read", {"file_path": small, "offset": 0}), None, {"CLAUDE_CORE_HAIKU_GUARD": "0"}, '"offset": 1'),
            ("offset 1 left alone", [assistant("m1", S, 20000, [("t9", "Read", {"file_path": small, "offset": 1})])],
             pre("Read", {"file_path": small, "offset": 1}), None, None, ""),
            ("deny wins over the offset fix", [assistant("m1", H, 61000, [("t9", "Read", {"file_path": big, "offset": 0})])],
             pre("Read", {"file_path": big, "offset": 0}), "a1", None, "Context budget"),
            ("main: compacted since last request", [assistant("m1", H, 72000, [("t1", "Read", {"file_path": big})]),
                                                     user([{"type": "tool_result", "tool_use_id": "t1", "content": "y" * 40000}]),
                                                     {"type": "system", "subtype": "compact_boundary"}],
             pre("Read", {"file_path": big}), None, None, ""),
        ]
        session = [
            user("Read data1.txt and data2.txt in 400-line chunks, then list the MARKER lines."),
            assistant("m1", H, 15000, [("t1", "Read", {"file_path": "data1.txt", "offset": 1, "limit": 400})]),
            user([{"type": "tool_result", "tool_use_id": "t1", "content": "..."}]),
            assistant("m2", H, 34000, [("t2", "Read", {"file_path": "data1.txt", "offset": 401, "limit": 400})]),
            user([{"type": "tool_result", "tool_use_id": "t2", "content": "..."}]),
            {"type": "system", "subtype": "compact_boundary"},
            user("This session is being continued from a previous conversation...", isCompactSummary=True),
        ]
        sonnet_session = [dict(r, message=dict(r["message"], model=S)) if r.get("type") == "assistant" else r for r in session]
        cases += [
            ("compact: resume point", session, {"hook_event_name": "SessionStart", "source": "compact"}, None, None, "Read data1.txt 401+400"),
            ("compact: request kept verbatim", session, {"hook_event_name": "SessionStart", "source": "compact"}, None, None, "then list the MARKER lines"),
            ("compact: not Haiku", sonnet_session, {"hook_event_name": "SessionStart", "source": "compact"}, None, None, ""),
            ("startup: silent", session, {"hook_event_name": "SessionStart", "source": "startup"}, None, None, ""),
        ]
        for name, rows, hook, sub, env, expect in cases:
            n += 1
            case_dir = os.path.join(tmp, f"c{n}")
            os.makedirs(case_dir)
            if name != "missing transcript":
                code, out = run(case_dir, rows, hook, sub, env)
            else:
                hook = dict(hook, transcript_path=os.path.join(case_dir, "nope.jsonl"), cwd=case_dir)
                r = subprocess.run(["bash", HOOK], input=json.dumps(hook), capture_output=True, text=True, timeout=10)
                code, out = r.returncode, r.stdout
            ok = code == 0 and ((expect in out) if expect else out == "")
            if ok and expect and hook["hook_event_name"] == "PreToolUse":
                decision = json.loads(out)["hookSpecificOutput"].get("permissionDecision")
                ok = decision is None if expect in ("Turn limit", '"updatedInput"', '"offset": 1') else decision == "deny"
                if ok and expect == "Context budget":
                    ok = "updatedInput" not in out
            failed += not ok
            print(("ok    " if ok else "FAIL  ") + name + ("" if ok else f"  -> {out[:200]!r}"))
    print(f"\n{n - failed}/{n} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
