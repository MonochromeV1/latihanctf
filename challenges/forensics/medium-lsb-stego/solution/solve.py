#!/usr/bin/env python3
"""Forensics/Medium solver — read the LSBs of the RGB channels (row-major) and
reconstruct the null-terminated flag. Ignores the tEXt-chunk decoy."""
import os
import re
import sys

from PIL import Image

DIST = os.environ.get("CHALLENGE_DIST",
                      os.path.join(os.path.dirname(__file__), "..", "dist"))
IMG = os.path.join(DIST, "stego.png")


def main():
    img = Image.open(IMG).convert("RGB")
    bits = []
    for (r, g, b) in img.getdata():
        bits += [r & 1, g & 1, b & 1]
    out = bytearray()
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        if byte == 0:
            break
        out.append(byte)
        if out.endswith(b"}") and b"claude{" in out:
            break
    m = re.search(rb"claude\{[^}]+\}", bytes(out))
    if not m:
        print("no flag in LSB", file=sys.stderr)
        sys.exit(1)
    print(m.group(0).decode())


if __name__ == "__main__":
    main()
