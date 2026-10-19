---
type: regex
pattern: '^(?=.*(product_id|orphan))(?=.*\b(set|to)\b.*\bnull\b)(?!.*not null).*$'
flags: mi
match: not_contains
---
