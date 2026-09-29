# Where Was This Taken — writeup

**Real flag:** `claude{eiffel_tower_paris_france}`.

## Solve
`exiftool photo.jpg` → GPS 48.8584 N, 2.2945 E = the Eiffel Tower. The confirming
flag is in EXIF **UserComment**; ImageDescription names a different place (decoy).

```bash
CHALLENGE_DIST=../dist python3 solve.py
```

## Planted decoys (NOT accepted)
| Decoy | Location |
|-------|----------|
| `claude{statue_of_liberty_new_york}` | EXIF ImageDescription |
