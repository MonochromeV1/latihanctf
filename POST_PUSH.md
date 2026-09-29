# POST_PUSH — what to do after you push

LatihanCTF is fully built: **8 categories, 30 challenge entries, `make test` = 30/30
passing**, committed per category (9 commits). Nothing has been pushed.

> Heads-up on git state: the working tree was wiped mid-build, so the repo was
> re-`git init`'d. History is a fresh line of 9 commits on branch **`main`**, and
> `origin` is set to `https://github.com/MonochromeV1/latihanctf.git`. There is **no
> shared history** with whatever may already be on the remote.

## 0. Before you push (~2 min)
```bash
git log --oneline            # 9 commits, one per category + scaffold + boot2root/docs
make venv && make tools      # solver deps + confirm host tools
make test                    # expect: 30 passed, 0 failed
git status                   # clean
```
Secrets are gitignored (`.ctf/config`, `.env`, `.venv/`, `ctfd-data/`).

## 1. Push
```bash
git push -u origin main
```
If it's rejected as non-fast-forward (the remote has unrelated old commits) and you
intend your local build to be the source of truth:
```bash
git push -u origin main --force-with-lease   # ONLY if you mean to replace remote history
```

## 2. Deploy & smoke-test locally
```bash
make deploy                  # CTFd + all networked challenges up, all challenges imported
# open http://127.0.0.1:8000   (admin / ctfd_admin_pw)
make test                    # 30/30
make down                    # stop;  make clean = stop + wipe CTFd volumes
```

## 3. Verify inside CTFd
- All 30 challenges imported with correct categories & points (100/250/500/1000;
  Boot2Root user 250 / root 500).
- Submit a real flag → accepted. Submit a decoy (e.g. `claude{keep_looking_admin_backup}`)
  → rejected. (Only real flags are registered; decoys never are.)

## 4. Serving players (SECURITY — read this)
Everything binds to `127.0.0.1` and lives on an isolated Docker bridge with
per-container mem/pids/cpu limits. To let players in:
- Expose **only** what they need (CTFd on 8000, plus the networked challenge ports
  81xx/82xx/83xx/86xx/9001) by binding those to your LAN IP in `docker-compose.yml`.
- **Never** expose these deliberately-vulnerable targets to the public internet.
  The Boot2Root box and pwn/web/SSTI/SSRF services are RCE by design.

## 5. Reset between runs
```bash
make clean && make deploy               # fresh scoreboard + re-import
docker compose restart <service>        # reset one challenge's state
```

## 6. Add more challenges
See README → "Add a challenge". Then `make test FILTER=<slug>` and `make deploy`.

## 7. Optional: Boot2Root as a full VM
The container is the primary deliverable. For a VM, replicate the Dockerfile steps
in a Packer/Vagrant Debian build, or `docker export` the container FS into a bootable
image. Isolated network only.

## 8. Notes / gotchas
- **pwntools not used** (no wheel on Python 3.14) — pwn/crypto solvers use raw
  sockets + `struct`; addresses were pinned from the built binaries.
- **AI backend is pluggable**: defaults to an offline deterministic mock so it's
  solvable with no API key/GPU. Set `LLM_BACKEND=ollama|openai` (+ `LLM_MODEL`,
  `LLM_API_BASE`, `LLM_API_KEY`) for a real model. See `challenges/ai/README.md`.
- `challenges/pwn/hard-ret2libc-rop/dist/libc.so.6` is Debian glibc, shipped so the
  ret2libc solve has the exact libc.
- Delete `READ_ME_FIRST_BLOCKER.md` if it's still around (leftover from the incident).
