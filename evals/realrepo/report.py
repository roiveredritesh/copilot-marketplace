"""Summarize one plugin run: cost by model, subagent dispatches, hook denials, Steps check, final answer."""
import glob, json, os, sys
out, name = sys.argv[1], sys.argv[2]
d = json.load(open(out))
sid = d["session_id"]
main = glob.glob(os.path.expanduser(f"~/.claude/projects/*/{sid}.jsonl"))[0]
rows = lambda p: [json.loads(l) for l in open(p) if l.strip()]
def summary(path):
    seen, maxp, tools, denials, model = set(), 0, {}, [], ""
    for e in rows(path):
        m = e.get("message") or {}
        if e.get("type") == "assistant" and m.get("usage") and m.get("id") not in seen:
            seen.add(m["id"]); u = m["usage"]; model = m.get("model", model)
            maxp = max(maxp, u["input_tokens"] + u["cache_read_input_tokens"] + u["cache_creation_input_tokens"])
        for b in m.get("content") or [] if isinstance(m.get("content"), list) else []:
            if b.get("type") == "tool_use":
                k = b["name"] + (f"({b['input'].get('subagent_type')})" if b["name"] == "Agent" else "")
                tools[k] = tools.get(k, 0) + 1
            if b.get("type") == "tool_result" and "hook error" in str(b.get("content")):
                denials.append(str(b.get("content"))[:160].replace("\n", " "))
    return model, len(seen), maxp, tools, denials
model, n, maxp, tools, den = summary(main)
print(f"=== {name}: ${d['total_cost_usd']:.3f}  turns={d['num_turns']}  main {model} requests={n} max_prompt={maxp}")
print("  cost by model:", {k: round(v['costUSD'], 4) for k, v in d.get("modelUsage", {}).items()})
print("  main tools:", tools)
for p in sorted(glob.glob(os.path.join(main[:-6], "subagents", "*.jsonl"))):
    if p.endswith(".meta.json"): continue
    sm, sn, sp, st, sd = summary(p)
    print(f"  sub {os.path.basename(p)[:22]} {sm} requests={sn} max_prompt={sp} tools={st}" + (f" DENIED={sd}" if sd else ""))
for x in den: print("  main DENIED:", x)
stop = [e for e in rows(main) if e.get("type") == "system" and "stop" in str(e.get("subtype", "")).lower()]
blocks = [str(e)[:300] for e in rows(main) if "Steps" in str(e) and ("block" in str(e).lower()) and e.get("type") in ("system", "user", "attachment")]
if blocks: print("  steps-check:", blocks[-1][:300])
res = str(d.get("result") or "")
print("  RESULT:", res[:2500].replace("\n", "\n    "))
