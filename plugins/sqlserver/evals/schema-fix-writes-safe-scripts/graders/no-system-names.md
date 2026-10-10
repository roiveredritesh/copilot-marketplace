---
type: regex
target: trace
pattern: '"[^"]*\.sql"\s*,\s*"content"\s*:\s*"(?:[^"\\]|\\.)*(PK|FK|DF)__'
flags: i
match: not_contains
---
