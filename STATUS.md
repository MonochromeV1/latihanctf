# LatihanCTF — BUILD STATUS

## ⚑ GO / NO-GO

**GO — build COMPLETE.** All 8 categories built from a clean slate (2026-09-29→30)
and committed. **`make test` = 30/30 solvers PASS, 0 fail** (28 Jeopardy across 7
categories + 2 Boot2Root flags). Every solver recovers the exact real flag and
prints no decoy. **Not pushed** — awaiting your review (`git push` when ready).

Totals: 30 challenge entries · 8 categories · ~45 planted decoys · CTFd stack +
isolated network + per-container resource limits.

**`make deploy` verified:** CTFd boots and imports all **30 challenges** (4 per
Jeopardy category + 2 Boot2Root flags), confirmed via the CTFd API.

### Summary table

| Category   | Built | Solvers pass | Notes |
|------------|-------|--------------|-------|
| Web        | ✅ 4/4 | ✅ 4/4      | recon, UNION SQLi, SSTI RCE, SSRF→pickle RCE |
| PWN        | ✅ 4/4 | ✅ 4/4      | var overwrite, ret2win+fmt, ret2libc ROP, heap UAF |
| Reverse    | ✅ 4/4 | ✅ 4/4      | strcmp, XOR-stack keygen, bytecode VM, z3 keygen |
| Crypto     | ✅ 4/4 | ✅ 4/4      | single-byte XOR, RSA cube-root, ECB & CBC oracles |
| Forensics  | ✅ 4/4 | ✅ 4/4      | EXIF, LSB stego, header repair, pcap→stego→zip chain |
| OSINT      | ✅ 4/4 | ✅ 4/4      | GPS EXIF, username pivot, doc metadata, multi-hop |
| AI         | ✅ 4/4 | ✅ 4/4      | prompt leak, roleplay bypass, encode-past-filter, RAG inject (mock backend) |
| Boot2Root  | ✅ 2/2 | ✅ 2/2      | cmd-injection foothold → sudo/find privesc; user.txt + root.txt |

## PHASE 0 — preflight

| Item | Result |
|------|--------|
| docker | 28.5.2 ✓ |
| docker compose | 2.40.3 ✓ |
| docker daemon | `hello-world` ran ✓ |
| python3 | 3.14.7 (pwntools NOT installable → pwn solvers use raw socket/struct) |
| gcc | 16.2.0 ✓ |
| solver venv | requests, pycryptodome 3.23, Pillow 12.3, sympy 1.14, z3-solver 5.1, ctfcli 0.1.8 ✓ |
| tools present | objdump, strings, file, binwalk, exiftool, steghide, upx, sqlite3, curl, jq, nc ✓ |
| tools missing | `zsteg`, `volatility3` — NOT required (forensics designed around PIL/steghide/binwalk) |
| CTFd smoke | (pending) |

Installs performed this session:
- `python3 -m venv .venv` + `pip install requests pycryptodome Pillow sympy z3-solver ctfcli`

## Per-challenge status

| Challenge | Category | Difficulty | Solver passes? | Real flag verified? | #decoys |
|-----------|----------|------------|----------------|---------------------|---------|
| easy-robots-recon | web | easy | ✅ | ✅ `claude{r0bots_txt_is_only_the_start}` | 3 |
| medium-sqli-login | web | medium | ✅ | ✅ `claude{un10n_select_your_way_in}` | 3 |
| hard-ssti-notes | web | hard | ✅ | ✅ `claude{jinja2_ssti_to_rce_gg}` | 3 |
| insane-ssrf-deserialize | web | insane | ✅ | ✅ `claude{ssrf_then_unpickle_equals_pwn}` | 3 |
| easy-overflow-var | pwn | easy | ✅ | ✅ `claude{stack_var_overwrite_grants_access}` | 1 |
| medium-ret2win-fmt | pwn | medium | ✅ | ✅ `claude{ret2win_with_a_canary_leak}` | 2 |
| hard-ret2libc-rop | pwn | hard | ✅ | ✅ `claude{ret2libc_rop_chain_to_shell}` | 2 |
| insane-heap-tcache | pwn | insane | ✅ | ✅ `claude{uaf_overwrites_the_vtable_ptr}` | 2 |
| easy-strcmp-password | reverse | easy | ✅ | ✅ `claude{strcmp_is_the_first_lesson}` | 1 |
| medium-xor-stack | reverse | medium | ✅ | ✅ `claude{x0r_on_the_stack_with_a_key}` | 1 |
| hard-vm-bytecode | reverse | hard | ✅ | ✅ `claude{stack_vm_reversed_by_hand}` | 1 |
| insane-keygen-z3 | reverse | insane | ✅ | ✅ `claude{z3_solves_the_keygen_easily}` | 1 |
| easy-xor-caesar | crypto | easy | ✅ | ✅ `claude{single_byte_xor_is_trivial}` | 1 |
| medium-rsa-smalle | crypto | medium | ✅ | ✅ `claude{cube_root_small_e_rsa}` | 1 |
| hard-aes-ecb-oracle | crypto | hard | ✅ | ✅ `claude{ecb_penguin_byte_by_byte}` | 1 |
| insane-cbc-padding-oracle | crypto | insane | ✅ | ✅ `claude{cbc_padding_oracle_leaks_all}` | 1 |
| easy-exif-strings | forensics | easy | ✅ | ✅ `claude{exif_usercomment_holds_the_key}` | 2 |
| medium-lsb-stego | forensics | medium | ✅ | ✅ `claude{lsb_hides_in_plain_sight}` | 1 |
| hard-header-repair | forensics | hard | ✅ | ✅ `claude{fix_the_magic_bytes_to_read_me}` | 1 |
| insane-multistage | forensics | insane | ✅ | ✅ `claude{pcap_carve_stego_unzip_chain}` | 2 |
| easy-gps-exif | osint | easy | ✅ | ✅ `claude{eiffel_tower_paris_france}` | 1 |
| medium-username-pivot | osint | medium | ✅ | ✅ `claude{username_pivot_to_the_paste}` | 2 |
| hard-doc-metadata | osint | hard | ✅ | ✅ `claude{doc_metadata_led_to_the_mirror}` | 2 |
| insane-multihop | osint | insane | ✅ | ✅ `claude{four_hops_exif_user_paste_vault}` | 3 |
| easy-system-prompt | ai | easy | ✅ | ✅ `claude{prompt_leak_no_defense}` | 1 |
| medium-roleplay-bypass | ai | medium | ✅ | ✅ `claude{roleplay_jailbreak_bypass}` | 1 |
| hard-output-filter | ai | hard | ✅ | ✅ `claude{encode_to_beat_the_filter}` | 1 |
| insane-guardrails-judge | ai | insane | ✅ | ✅ `claude{indirect_injection_via_rag}` | 1 |
| easy-cmdinject (user.txt) | boot2root | easy | ✅ | ✅ `claude{foothold_via_command_injection}` | 2 |
| easy-cmdinject-root (root.txt) | boot2root | hard | ✅ | ✅ `claude{sudo_find_gtfobin_gets_root}` | 2 |

## Morning pre-push checklist

- [x] Full status table complete (all 30 entries above)
- [x] `make test` passes all solvers — **30/30 PASS, 0 fail**
- [x] `grep -rn "claude{" challenges/*/*/dist/` classified — real flags in dist ONLY
      for intended-artifact challenges (forensics-easy EXIF, osint easy/medium/hard);
      RE/PWN/crypto/boot2root ship only decoys, real flags encoded/server-side
- [x] `find . -size +50M` — none (largest: `pwn/hard-ret2libc-rop/dist/libc.so.6` ~1.9 MB)
- [ ] **DID NOT PUSH** — left for your review. See `POST_PUSH.md` for next steps.

## How to review & run
```bash
make venv && make tools     # solver deps + host-tool check
make deploy                 # CTFd up + import all challenges (http://127.0.0.1:8000)
make test                   # re-run every solver (expect 30/30)
```
CTFd admin: `admin` / `ctfd_admin_pw` (set by scripts/setup_ctfd.py).
