#!/usr/bin/env python3
"""Generate photo.jpg with GPS EXIF pointing at a landmark. Real flag (the
landmark) is in UserComment; a wrong-location decoy is in ImageDescription."""
import os
import subprocess

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "dist", "photo.jpg")
REAL = "claude{eiffel_tower_paris_france}"
DECOY = "claude{statue_of_liberty_new_york}"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
Image.new("RGB", (600, 400), (120, 140, 160)).save(OUT, "JPEG", quality=88)

# GPS for the Eiffel Tower; UserComment holds the flag; ImageDescription a decoy.
subprocess.run(["exiftool", "-overwrite_original",
                "-GPSLatitude=48.8584", "-GPSLatitudeRef=N",
                "-GPSLongitude=2.2945", "-GPSLongitudeRef=E",
                f"-UserComment={REAL}",
                f"-ImageDescription=vacation photo near {DECOY}",
                OUT], check=True, stdout=subprocess.DEVNULL)
print("wrote", OUT)
