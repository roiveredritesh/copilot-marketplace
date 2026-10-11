"""Unit tests for plugins/core/hooks/steps-check.sh (Stop hook). No model calls, free to run.
usage: python evals/steps_check_test.py"""
import json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(ROOT, "plugins", "core", "hooks", "steps-check.sh")

CMD = {"type": "user", "message": {"role": "user", "content": "<command-name>/dotnet:analyze</command-name> x"}}


def agent(kind):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Agent", "input": {"subagent_type": f"core:{kind}", "prompt": "WORK ORDER"}}]}}


def tool(name, **inp):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": name, "input": inp}]}}


def result(text):
    return {"type": "user", "message": {"content": [{"type": "tool_result", "content": text}]}}


def note(text):  # background agent hand-back, arrives as a plain user message
    return {"type": "user", "message": {"content": text}}


def say(text):
    return {"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}}


def run(entries, cwd, active=False):
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
        f.write("\n".join(json.dumps(e) for e in entries))
    payload = json.dumps({"hook_event_name": "Stop", "transcript_path": f.name, "cwd": cwd, "stop_hook_active": active})
    out = subprocess.run(["bash", HOOK], input=payload, capture_output=True, text=True).stdout.strip()
    os.unlink(f.name)
    return "block" if out and json.loads(out).get("decision") == "block" else "allow"


def main():
    cwd = tempfile.mkdtemp()
    os.makedirs(os.path.join(cwd, ".reports"))
    open(os.path.join(cwd, ".reports", "analysis-x.md"), "w").close()
    old_scout = [CMD, agent("scout"), say("Steps: scout=dispatched")]
    cases = [
        ("honest analyze", [CMD, agent("scout"), agent("runner"), tool("Read"), tool("Read"),
                            say("done\n\nSteps: scout=dispatched runner=dispatched verified=2 refs opened file=.reports/analysis-x.md")], "allow"),
        ("background hand-back later", [CMD, agent("scout"), say("waiting"), note("[Subagent hand-back] found 3 facts"),
                                        say("Steps: scout=dispatched")], "allow"),
        ("runner claimed, not dispatched", [CMD, agent("scout"), say("Steps: scout=dispatched runner=dispatched")], "block"),
        ("scout from an earlier command doesn't count", old_scout + [CMD, say("Steps: scout=dispatched")], "block"),
        ("missing file", [CMD, agent("scout"), say("Steps: scout=dispatched file=.reports/nope.md")], "block"),
        ("file skipped with reason", [CMD, say("Steps: scout=not needed (no existing code) file=skipped (user said no)")], "allow"),
        ("gate claimed, never asked", [CMD, say("Steps: audit=4 findings gate=asked: Fix all db-writes=none")], "block"),
        ("gate asked", [CMD, tool("AskUserQuestion", questions=[]), say("Steps: audit=4 findings gate=asked: Fix all db-writes=none")], "allow"),
        ("verified more than read", [CMD, agent("scout"), tool("Read"), say("Steps: scout=dispatched verified=3 refs opened")], "block"),
        ("tests passed, unbacked", [CMD, agent("runner"), result("TESTS FAILED (2)"), say("Steps: mode=tdd final=TESTS PASSED")], "block"),
        ("tests passed, backed", [CMD, agent("runner"), result("STATUS: TESTS PASSED (14)"), say("Steps: mode=tdd final=TESTS PASSED")], "allow"),
        ("review dispatched list", [CMD, agent("scout"), agent("runner"), say("Steps: scope=main..HEAD dispatched=scout, runner, reviewer verified=0")], "block"),
        ("no Steps line", [CMD, say("Here is a plain answer.")], "allow"),
        ("Steps line not in the final message", [CMD, say("Steps: runner=dispatched"), say("Anything else?")], "allow"),
    ]
    failed = 0
    for name, entries, want in cases:
        got = run(entries, cwd)
        failed += got != want
        print(f"{'ok  ' if got == want else 'FAIL'} {want:5} {got:5} {name}")
    got = run([CMD, say("Steps: runner=dispatched")], cwd, active=True)
    failed += got != "allow"
    print(f"{'ok  ' if got == 'allow' else 'FAIL'} allow {got:5} second stop never blocks (stop_hook_active)")
    print(f"\n{len(cases) + 1 - failed}/{len(cases) + 1} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
