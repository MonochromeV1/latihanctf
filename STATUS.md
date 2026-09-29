# LatihanCTF — BUILD STATUS

## ⚑ GO / NO-GO

**PHASE 0: GO.** Rebuilt from a clean slate on 2026-09-29 (previous tree + git
history were intentionally wiped at the user's explicit request). Tooling,
Docker, and the solver venv are healthy.

> Note: this is a full from-scratch rebuild. Categories are (re)built and
> committed one at a time; solvers are run end-to-end before each commit.
> **Not pushed** — awaiting morning review.

### Summary table

| Category   | Built | Solvers pass | Notes |
|------------|-------|--------------|-------|
| Web        | ✅ 4/4 | ✅ 4/4      | recon, UNION SQLi, SSTI RCE, SSRF→pickle RCE |
| PWN        | ⏳    | –            | in progress |
| Reverse    | ⏳    | –            | |
| Crypto     | ⏳    | –            | |
| Forensics  | ⏳    | –            | |
| OSINT      | ⏳    | –            | |
| AI         | ⏳    | –            | |
| Boot2Root  | ⏳    | –            | |

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

## Morning pre-push checklist

- [ ] Full status table complete
- [ ] `make test` passes all solvers
- [ ] `grep -rn "claude{" challenges/*/*/dist/` classified (real / decoy / intended-artifact)
- [ ] `find . -size +50M` (flag files near GitHub's 100 MB limit)
- [ ] **DO NOT PUSH** until reviewed
