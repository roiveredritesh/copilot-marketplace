---
type: regex
target: trace
pattern: '"[^"]*\.sql"\s*,\s*"content"\s*:\s*"(?:[^"\\]|\\.)*WITH NOCHECK ADD'
flags: i
match: not_contains
---
