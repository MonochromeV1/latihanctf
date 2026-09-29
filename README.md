# LatihanCTF

A self-hosted, Jeopardy-style Capture-The-Flag built on **CTFd**. Every target is
intentionally vulnerable and meant to run **locally, on an isolated network, for
authorized private/educational use only**.

> ⚠️ **SECURITY.** These containers are deliberately exploitable (RCE, SQLi,
> memory-corruption, a root-me box, prompt-injectable LLM apps). They publish
> **only to `127.0.0.1`** and sit on an isolated Docker bridge network. **Never**
> expose them to a hostile or public network, and never run them on a machine you
> care about without understanding the risk.

Flag format: `claude{lower_snake_case}` — e.g. `claude{ret2win_is_the_way}`.
Points: **Easy 100 · Medium 250 · Hard 500 · Insane 1000.**

## Categories

Web · PWN · Reverse Engineering · Cryptography · Forensics · OSINT ·
AI/Prompt-Injection · Boot2Root. Four tiers each (Easy→Insane), plus a Boot2Root
machine with two flags. See `ctf.yml` for the full manifest.

Every challenge (except trivial Easy) plants **decoy flags** — plausible
`claude{...}` strings that CTFd does **not** accept — to punish grep-only solving.
Each `solution/WRITEUP.md` lists the real flag and every decoy.

## Quick start

```bash
make venv          # one-time: solver virtualenv (.venv)
make up            # start CTFd + all networked challenges
make deploy        # start + import every challenge into CTFd
# open http://127.0.0.1:8000  (admin / ctfd_admin_pw)
make test          # run every automated solver end-to-end
make down          # stop; `make clean` also drops volumes
```

`make test FILTER=web` runs only matching challenges.

## Repository layout

```
challenges/<category>/<difficulty>-<slug>/
  challenge.yml        # ctfcli-style: name, category, value, description, flags, files
  dist/                # ONLY what players download
  src/                 # full source + Dockerfile + build scripts
  solution/
    WRITEUP.md         # step-by-step solve + list of planted decoys
    solve.py|solve.sh  # automated solver — prints the EXACT real flag, never a decoy
    decoys.txt         # machine-readable decoy list (used by the test harness)
    meta.yml           # test metadata: kind (file/net), service, port, url
docker-compose.yml     # CTFd + all networked challenges (isolated net, resource limits)
scripts/               # setup_ctfd.py (import), run_solvers.py (test harness)
ctf.yml  Makefile  STATUS.md
```

`dist/` never contains a real flag in plaintext **except** where reading the
artifact *is* the challenge (EXIF/GPS in easy Forensics/OSINT). RE/PWN/Crypto/
Boot2Root flags are computed or server-side only.

## Add a challenge

1. `mkdir -p challenges/<cat>/<tier>-<slug>/{dist,src,solution}`
2. Write `challenge.yml` (name, category, value, description, `flags:` = the real
   flag only, `files:` = paths under the challenge dir served to players).
3. Put player-facing files in `dist/`, full source + `Dockerfile` in `src/`.
4. Write `solution/WRITEUP.md` (+ decoys), `solution/decoys.txt`, `solve.py`, and
   `solution/meta.yml`.
5. If networked, add a service to `docker-compose.yml` (publish to `127.0.0.1`,
   inherit the `*chal` resource limits).
6. `make test FILTER=<slug>` then `make deploy`.

## Reset

```bash
make clean         # stop stack + delete CTFd volumes (fresh scoreboard)
make deploy        # re-import from scratch
```

To reset a single challenge's state, `docker compose restart <service>`.

## LLM backend for AI challenges (pluggable)

The AI category talks to an LLM chosen by env var, defaulting to a deterministic
**mock** backend so the challenges are solvable with no API key or GPU:

```bash
# deterministic mock (default, offline)
LLM_BACKEND=mock make up
# local Ollama
LLM_BACKEND=ollama LLM_MODEL=llama3 LLM_API_BASE=http://host.docker.internal:11434 make up
# OpenAI-compatible / Anthropic-compatible API
LLM_BACKEND=openai LLM_MODEL=gpt-4o-mini LLM_API_BASE=https://api.openai.com/v1 LLM_API_KEY=sk-... make up
```

See `challenges/ai/README.md` for details.
