---
type: regex
target: { source: file, path: .git/eval-fake/calls.log }
pattern: '^WRITE'
flags: m
match: not_contains
---
