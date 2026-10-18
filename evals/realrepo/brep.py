"""Byte-exact replace that keeps the file's line endings and BOM."""
import sys
p, a, b = sys.argv[1], sys.argv[2].encode(), sys.argv[3].encode()
s = open(p, "rb").read()
crlf = b"\r\n" in s
if crlf:
    a, b = a.replace(b"\n", b"\r\n"), b.replace(b"\n", b"\r\n")
assert s.count(a) == 1, (p, a)
open(p, "wb").write(s.replace(a, b))
