#!/usr/bin/env python3
"""OSINT/Easy solver — the GPS in EXIF points at the landmark; the confirming
flag is in UserComment (ImageDescription holds a decoy location)."""
import os
import re
import subprocess
import sys

DIST = os.environ.get("CHALLENGE_DIST",
                      os.path.join(os.path.dirname(__file__), "..", "dist"))
IMG = os.path.join(DIST, "photo.jpg")


def main():
    # GPS is the clue:
    gps = subprocess.check_output(["exiftool", "-s3", "-GPSLatitude", "-GPSLongitude", IMG]).decode()
    # flag confirmed in UserComment:
    uc = subprocess.check_output(["exiftool", "-s3", "-UserComment", IMG]).decode()
    m = re.search(r"claude\{[^}]+\}", uc)
    if not m:
        print("no flag in UserComment; gps was:\n" + gps, file=sys.stderr)
        sys.exit(1)
    print(m.group(0))


if __name__ == "__main__":
    main()
