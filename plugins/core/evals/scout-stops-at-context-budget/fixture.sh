#!/usr/bin/env bash
# Five ~140 KB files (~70K tokens each on Haiku 5.5): reading them all would cross the 60K work-order budget.
set -e
py=python3; command -v python3 >/dev/null 2>&1 || py=python
"$py" - <<'PY'
import random
random.seed(7)
words = "alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo lima mike".split()
for i in range(1, 6):
    with open(f"data{i}.txt", "w") as f:
        for n in range(1, 1601):
            line = f"MARKER{i} value={1000 * i + 7}" if n == 1500 else " ".join(random.choice(words) + str(random.randint(0, 999)) for _ in range(9))
            f.write(f"{n:04d} {line}\n")
PY
g() { git -c core.autocrlf=false -c user.name=eval -c user.email=eval@example.com "$@"; }
g init -q && g add -A && g commit -qm "fixture"
