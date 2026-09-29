#!/usr/bin/env python3
"""Forensics/Hard solver — repair the zeroed PNG signature, then read the
compressed zTXt chunk (which strings can't see). Ignores the plaintext tEXt decoy."""
import io
import os
import re
import sys

from PIL import Image

DIST = os.environ.get("CHALLENGE_DIST",
                      os.path.join(os.path.dirname(__file__), "..", "dist"))
IMG = os.path.join(DIST, "broken.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
DECOY = "claude{plaintext_text_chunk_decoy}"


def main():
    data = bytearray(open(IMG, "rb").read())
    data[0:8] = PNG_MAGIC                      # repair signature
    img = Image.open(io.BytesIO(bytes(data)))
    img.load()
    # img.text holds both tEXt and (decompressed) zTXt values
    for k, v in img.text.items():
        for m in re.findall(r"claude\{[^}]+\}", v):
            if m != DECOY:
                print(m)
                return
    print("no flag after repair", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
