# Broken Signature — writeup

**Real flag:** `claude{fix_the_magic_bytes_to_read_me}` — in a compressed zTXt chunk.

## Solve
The first 8 bytes (PNG signature) are zeroed. Restore them to
`89 50 4E 47 0D 0A 1A 0A`, then parse the PNG. The flag is in a **zTXt**
(zlib-compressed) text chunk — invisible to `strings`. Any PNG parser (e.g. PIL)
decompresses it: read `img.text`.

```bash
CHALLENGE_DIST=../dist python3 solve.py
```

## Planted decoys (NOT accepted)
| Decoy | Location |
|-------|----------|
| `claude{plaintext_text_chunk_decoy}` | plaintext tEXt chunk (`strings` shows it without repair) |
