#!/usr/bin/env python3
"""Crypto/Medium solver — e=3 with no padding and m^3 < n, so c is a perfect
cube: m = cuberoot(c). Uses the real `c` (not the c_backup decoy). Prints only
the real flag."""
import os
import re
import sys

from sympy import integer_nthroot

DIST = os.environ.get("CHALLENGE_DIST",
                      os.path.join(os.path.dirname(__file__), "..", "dist"))


def long_to_bytes(n):
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return b


def main():
    text = open(os.path.join(DIST, "params.txt")).read()
    c = int(re.search(r"^c\s*=\s*(\d+)", text, re.M).group(1))
    m, exact = integer_nthroot(c, 3)
    pt = long_to_bytes(m)
    fl = re.search(rb"claude\{[^}]+\}", pt)
    if not fl:
        print("cube root did not yield a flag", file=sys.stderr)
        sys.exit(1)
    print(fl.group(0).decode())


if __name__ == "__main__":
    main()
