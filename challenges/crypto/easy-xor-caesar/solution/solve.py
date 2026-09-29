#!/usr/bin/env python3
"""Crypto/Easy solver — brute-force the single-byte XOR key over the hex payload.
Ignores the base64 decoy. Prints only the real flag."""
import os
import re
import sys

DIST = os.environ.get("CHALLENGE_DIST",
                      os.path.join(os.path.dirname(__file__), "..", "dist"))
DECOY = "claude{base64_is_not_xor}"


def main():
    text = open(os.path.join(DIST, "cipher.txt")).read()
    hexline = re.search(r"\b([0-9a-fA-F]{20,})\b", text).group(1)
    ct = bytes.fromhex(hexline)
    for k in range(256):
        pt = bytes(b ^ k for b in ct)
        m = re.fullmatch(rb"claude\{[ -~]+\}", pt)
        if m and DECOY.encode() not in pt:
            print(pt.decode())
            return
    print("no flag", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
