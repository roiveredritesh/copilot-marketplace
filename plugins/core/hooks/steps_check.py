"""Stop hook: check the skill's `Steps:` line against what actually happened in the transcript.

A claim like `scout=dispatched` must match a real core:scout Agent call, `gate=asked` a real
AskUserQuestion, `file=<path>` a file on disk, `final=TESTS PASSED` a tool result that says so.
A false claim blocks the stop once, with the reason, so the model fixes the work or the line.
Never breaks a session: any error, or no Steps line, means allow."""
import json, os, re, sys

AGENTS = ("scout", "runner", "reviewer", "publisher")
ASK_KEYS = ("gate", "choice", "confirm", "questions", "tests")
FILE_KEYS = ("file", "files", "saved")
STATUS_KEYS = ("final", "suite", "run")
STATUSES = ("TESTS PASSED", "BUILD OK")


def load(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                out.append(json.loads(line))
            except ValueError:
                pass
    return out


def scope(entries):
    """Entries since the last slash command (background results arrive as later user messages)."""
    start = 0
    for i, e in enumerate(entries):
        c = e.get("message", {}).get("content") if e.get("type") == "user" else None
        if isinstance(c, str) and "<command-name>" in c:
            start = i
    return [e for e in entries[start:] if e.get("type") in ("user", "assistant") and not e.get("isSidechain")]


def blocks(e):
    c = e.get("message", {}).get("content")
    return [{"type": "text", "text": c}] if isinstance(c, str) else (c or [])


def steps_line(entries):
    """The Steps line of the final assistant text, or None."""
    for e in reversed(entries):
        if e["type"] != "assistant":
            continue
        texts = [b.get("text", "") for b in blocks(e) if b.get("type") == "text"]
        if not texts:
            continue
        m = re.search(r"Steps:\s*(.+)", "\n".join(texts))
        return m.group(1).strip().strip("`").strip() if m else None
    return None


def parse(line):
    """`a=x y=two words (why) z=w` -> {a: 'x', y: 'two words (why)', z: 'w'}"""
    return dict(p.split("=", 1) for p in re.split(r"\s+(?=[a-z][\w-]*=)", line) if "=" in p)


def check(claims, entries, cwd):
    agents, asked, reads, results = set(), False, 0, []
    for e in entries:
        for b in blocks(e):
            if b.get("type") == "tool_use":
                name, inp = b.get("name"), b.get("input") or {}
                if name in ("Agent", "Task"):
                    agents.add(str(inp.get("subagent_type", "")).split(":")[-1])
                elif name == "AskUserQuestion":
                    asked = True
                elif name == "Read":
                    reads += 1
            elif b.get("type") == "tool_result":
                c = b.get("content")
                results.append(c if isinstance(c, str) else json.dumps(c))
            elif b.get("type") == "text" and e["type"] == "user":
                results.append(b.get("text", ""))  # subagent hand-backs and task notifications
    seen = "\n".join(results)
    bad = []
    for key, val in claims.items():
        v = val.strip().strip("`")
        if key in AGENTS and v.startswith("dispatched") and key not in agents:
            bad.append(f"{key}=dispatched, but no core:{key} Agent call happened")
        elif key == "dispatched":
            for name in re.findall(r"[a-z]+", v):
                if name in AGENTS and name not in agents:
                    bad.append(f"dispatched lists {name}, but no core:{name} Agent call happened")
        elif key in ASK_KEYS and v.startswith("asked") and not asked:
            bad.append(f"{key}=asked, but AskUserQuestion was never called")
        elif key in FILE_KEYS and not re.match(r"(no|none|skipped|n/a)\b", v):
            for p in re.split(r"[,\s]+", v):
                p = p.strip("`'\"()")
                if ("/" in p or "." in p) and not os.path.exists(os.path.join(cwd, p)):
                    bad.append(f"{key}={p}, but that file doesn't exist")
        elif key == "verified":
            n = re.match(r"(\d+)", v)
            if n and reads < int(n.group(1)):
                bad.append(f"verified={n.group(1)} refs, but only {reads} Read calls happened")
        elif key in STATUS_KEYS:
            for s in STATUSES:
                if s in v and s not in seen:
                    bad.append(f"{key} says {s}, but no tool result contains it")
    return bad


def main():
    try:
        hook = json.load(sys.stdin)
        if hook.get("stop_hook_active"):
            return  # already nudged once; never loop
        entries = scope(load(hook["transcript_path"]))
        line = steps_line(entries)
        if not line:
            return
        bad = check(parse(line), entries, hook.get("cwd") or os.getcwd())
        if bad:
            print(json.dumps({"decision": "block", "reason":
                "ritesh-marketplace steps check: the Steps line doesn't match what happened: " + "; ".join(bad)
                + ". Do the missing step now, or correct the Steps line to say skipped (<reason>)."}))
    except Exception:
        pass


if __name__ == "__main__":
    main()
