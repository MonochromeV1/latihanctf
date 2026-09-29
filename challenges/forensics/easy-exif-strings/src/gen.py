#!/usr/bin/env python3
"""Generate evidence.jpg: real flag in EXIF UserComment; decoys in EXIF Artist and
an appended plaintext trailer (what a strings-only solver grabs first)."""
import os
import subprocess

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "dist", "evidence.jpg")
REAL = "claude{exif_usercomment_holds_the_key}"
DECOY_ARTIST = "claude{exif_artist_decoy}"
DECOY_TRAILER = "claude{just_reading_strings_decoy}"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img = Image.new("RGB", (640, 480), (30, 60, 90))
for y in range(480):
    for x in range(0, 640, 32):
        img.putpixel((x, y), (200, 200, 50))
img.save(OUT, "JPEG", quality=85)

subprocess.run(["exiftool", "-overwrite_original",
                f"-UserComment={REAL}", f"-Artist={DECOY_ARTIST}",
                "-Make=CanonSpy", "-Model=EOS-Evidence", OUT], check=True,
               stdout=subprocess.DEVNULL)

with open(OUT, "ab") as f:
    f.write(b"\n<!-- field note: " + DECOY_TRAILER.encode() + b" -->\n")

print("wrote", OUT)
