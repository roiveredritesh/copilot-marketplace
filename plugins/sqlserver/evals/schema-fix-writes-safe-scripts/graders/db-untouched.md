---
type: regex
target: { source: file, path: .git/eval-fake/calls.log }
pattern: '^(DDL|NOT_READONLY)'
flags: m
match: not_contains
---
