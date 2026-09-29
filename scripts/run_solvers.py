#!/usr/bin/env python3
"""LatihanCTF solver test harness.

For each challenge that has solution/meta.yml, this:
  1. reads the REAL flag(s) from challenge.yml
  2. reads planted decoys from solution/decoys.txt
  3. brings the challenge container up (kind: net) if needed
  4. runs the automated solver
  5. asserts the solver's LAST claude{...} equals a real flag
     AND that NO decoy string appears anywhere in solver output

Usage:
  python3 scripts/run_solvers.py [substring-filter ...]
Exit code 0 iff every selected solver passes.
"""
import os
import re
import subprocess
import sys
import time
import socket
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required (use the .venv python).", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
CHAL = ROOT / "challenges"
FLAG_RE = re.compile(r"claude\{[^}]*\}")
PYTHON = os.environ.get("SOLVER_PYTHON", str(ROOT / ".venv" / "bin" / "python"))
if not Path(PYTHON).exists():
    PYTHON = sys.executable


def load_yaml(p):
    with open(p) as f:
        return yaml.safe_load(f)


def real_flags(chal_dir):
    y = load_yaml(chal_dir / "challenge.yml")
    flags = y.get("flags", []) or []
    out = []
    for fl in flags:
        if isinstance(fl, dict):
            out.append(fl.get("content", ""))
        else:
            out.append(str(fl))
    return [f for f in out if f]


def decoys(chal_dir):
    p = chal_dir / "solution" / "decoys.txt"
    if not p.exists():
        return []
    return [ln.strip() for ln in p.read_text().splitlines()
            if ln.strip() and ln.strip().startswith("claude{")]


def port_open(host, port, timeout=1.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def wait_port(host, port, tries=60):
    for _ in range(tries):
        if port_open(host, port):
            return True
        time.sleep(1)
    return False


def compose_up(service):
    subprocess.run(
        ["docker", "compose", "up", "-d", "--build", service],
        cwd=ROOT, check=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
    )


def run_one(chal_dir):
    meta_p = chal_dir / "solution" / "meta.yml"
    if not meta_p.exists():
        return None  # not a testable challenge yet
    meta = load_yaml(meta_p) or {}
    rf = real_flags(chal_dir)
    dc = decoys(chal_dir)
    solver = meta.get("solver", "solve.py")
    solver_path = chal_dir / "solution" / solver
    if not solver_path.exists():
        return (False, f"solver {solver} missing")

    env = dict(os.environ)
    env["CHALLENGE_DIST"] = str(chal_dir / "dist")
    kind = meta.get("kind", "file")
    if kind == "net":
        host = meta.get("host", "127.0.0.1")
        port = int(meta["port"])
        if not port_open(host, port):
            svc = meta.get("service")
            if svc:
                try:
                    compose_up(svc)
                except subprocess.CalledProcessError as e:
                    return (False, f"compose up {svc} failed: {e}")
            if not wait_port(host, port):
                return (False, f"service not reachable on {host}:{port}")
            time.sleep(3)  # let the app finish starting after the port opens
        env["CHALLENGE_HOST"] = host
        env["CHALLENGE_PORT"] = str(port)
        env["CHALLENGE_URL"] = meta.get("url", f"http://{host}:{port}/")

    if solver.endswith(".sh"):
        cmd = ["bash", str(solver_path)]
    else:
        cmd = [PYTHON, str(solver_path)]
    try:
        proc = subprocess.run(cmd, cwd=chal_dir / "solution", env=env,
                              capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        return (False, "solver timed out")
    out = proc.stdout + "\n" + proc.stderr
    found = FLAG_RE.findall(out)
    if not found:
        return (False, f"no flag in solver output (rc={proc.returncode})")
    # decoy leak check
    for d in dc:
        if d in out:
            return (False, f"solver leaked decoy {d}")
    last = found[-1]
    if last not in rf:
        return (False, f"last flag {last} != real flag {rf}")
    return (True, last)


def discover(filters):
    dirs = []
    for cy in sorted(CHAL.glob("*/*/challenge.yml")):
        d = cy.parent
        rel = str(d.relative_to(ROOT))
        if filters and not any(f in rel for f in filters):
            continue
        dirs.append(d)
    return dirs


def main():
    filters = sys.argv[1:]
    dirs = discover(filters)
    if not dirs:
        print("No challenges match.")
        return 0
    npass = nfail = nskip = 0
    rows = []
    for d in dirs:
        rel = str(d.relative_to(CHAL))
        res = run_one(d)
        if res is None:
            nskip += 1
            rows.append((rel, "SKIP", "no meta.yml"))
            continue
        ok, msg = res
        if ok:
            npass += 1
            rows.append((rel, "PASS", msg))
        else:
            nfail += 1
            rows.append((rel, "FAIL", msg))
    w = max(len(r[0]) for r in rows)
    for rel, st, msg in rows:
        mark = {"PASS": "✓", "FAIL": "✗", "SKIP": "-"}[st]
        print(f"  {mark} {rel.ljust(w)}  {st}  {msg}")
    print(f"\n{npass} passed, {nfail} failed, {nskip} skipped")
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main())
