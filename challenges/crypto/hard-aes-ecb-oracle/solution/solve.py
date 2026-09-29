#!/usr/bin/env python3
"""Crypto/Hard solver — classic ECB byte-at-a-time decryption of the appended
SECRET. Prints only the real flag."""
import os
import re
import sys

import requests

URL = os.environ.get("CHALLENGE_URL", "http://127.0.0.1:8303/").rstrip("/") + "/"
BS = 16
DECOY = "claude{ecb_mode_hides_nothing_decoy}"


def oracle(data: bytes) -> bytes:
    r = requests.get(URL + "encrypt", params={"data": data.hex()}, timeout=10)
    return bytes.fromhex(r.text.strip())


def main():
    known = b""
    total = len(oracle(b""))          # length of ECB(pad(SECRET))
    for _ in range(total):
        pad_len = (BS - 1 - (len(known) % BS)) % BS
        prefix = b"A" * pad_len
        blk = (pad_len + len(known)) // BS
        target = oracle(prefix)[blk * BS:(blk + 1) * BS]
        found = False
        for g in range(256):
            trial = prefix + known + bytes([g])
            if oracle(trial)[blk * BS:(blk + 1) * BS] == target:
                known += bytes([g])
                found = True
                break
        if not found:
            break
        if known.endswith(b"}") and b"claude{" in known:
            break
    m = re.search(rb"claude\{[^}]+\}", known)
    if not m or m.group(0).decode() == DECOY:
        print("recovery failed", file=sys.stderr)
        sys.exit(1)
    print(m.group(0).decode())


if __name__ == "__main__":
    main()
