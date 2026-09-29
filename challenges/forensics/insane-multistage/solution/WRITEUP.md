# Drop Chain — writeup

**Real flag:** `claude{pcap_carve_stego_unzip_chain}` — inside the encrypted zip.

## Kill chain
1. **pcap** — the HTTP request leaks `X-Steg-Pass: st3g0_pass`. Follow the two
   HTTP responses and carve the bodies: `stego.jpg` (FF D8…) and `secret.zip` (PK…).
2. **steghide** — `steghide extract -sf stego.jpg -p st3g0_pass` → `hint.txt`
   containing `zip password: Sw0rdf1sh_2024`.
3. **zip** — open `secret.zip` with that password → `flag.txt`.

```bash
CHALLENGE_DIST=../dist python3 solve.py
```

## Planted decoys (NOT accepted)
| Decoy | Location |
|-------|----------|
| `claude{pcap_plaintext_decoy}` | `X-Note` header in the pcap (`strings`) |
| `claude{wrong_file_in_the_archive}` | `readme.txt` inside `secret.zip` |
