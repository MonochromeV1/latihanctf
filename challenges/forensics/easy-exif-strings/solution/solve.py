#!/usr/bin/env python3
"""Forensics/Easy solver — pull the flag from the EXIF UserComment field (not the
Artist field or the appended trailer, which are decoys)."""
import os
import re
import subprocess
import sys

DIST = os.environ.get("CHALLENGE_DIST",
                      os.path.join(os.path.dirname(__file__), "..", "dist"))
IMG = os.path.join(DIST, "evidence.jpg")


def main():
    out = subprocess.check_output(["exiftool", "-s3", "-UserComment", IMG]).decode()
    m = re.search(r"claude\{[^}]+\}", out)
    if not m:
        print("no flag in UserComment", file=sys.stderr)
        sys.exit(1)
    print(m.group(0))


if __name__ == "__main__":
    main()
