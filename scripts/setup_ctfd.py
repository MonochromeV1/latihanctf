#!/usr/bin/env python3
"""Bootstrap CTFd and import every challenge via the REST API.

- Performs first-run /setup (admin user, event name) if needed.
- Logs in, creates an API token, writes it to .ctf/config (gitignored).
- Imports each challenges/*/*/challenge.yml: challenge + REAL flag(s) + files.
  (Decoys are NEVER registered as flags.)

Idempotent-ish: skips challenges whose name already exists.
"""
import configparser
import glob
import os
import re
import sys
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
BASE = os.environ.get("CTFD_URL", "http://127.0.0.1:8000")
ADMIN_USER = os.environ.get("CTFD_ADMIN", "admin")
ADMIN_PASS = os.environ.get("CTFD_ADMIN_PASS", "ctfd_admin_pw")
ADMIN_EMAIL = os.environ.get("CTFD_ADMIN_EMAIL", "admin@latihanctf.local")
CTF_NAME = os.environ.get("CTFD_NAME", "LatihanCTF")

NONCE_RE = re.compile(r"name=['\"]nonce['\"]\s+value=['\"]([0-9a-f]+)['\"]", re.I)


def nonce(session, path):
    r = session.get(BASE + path)
    m = NONCE_RE.search(r.text)
    return m.group(1) if m else None


def is_setup(session):
    r = session.get(BASE + "/setup", allow_redirects=False)
    # once configured, /setup redirects (302) to /
    return r.status_code in (301, 302)


def do_setup(session):
    n = nonce(session, "/setup")
    data = {
        "ctf_name": CTF_NAME,
        "ctf_description": "Self-hosted educational CTF (authorized use only).",
        "user_mode": "users",
        "challenge_visibility": "private",
        "account_visibility": "public",
        "score_visibility": "public",
        "registration_visibility": "public",
        "verify_emails": "false",
        "name": ADMIN_USER,
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASS,
        "ctf_theme": "core-beta",
        "nonce": n,
    }
    r = session.post(BASE + "/setup", data=data, allow_redirects=True)
    r.raise_for_status()
    print("[+] CTFd initial setup complete")


def login(session):
    n = nonce(session, "/login")
    r = session.post(BASE + "/login",
                     data={"name": ADMIN_USER, "password": ADMIN_PASS, "nonce": n},
                     allow_redirects=True)
    if "incorrect" in r.text.lower():
        raise SystemExit("[-] admin login failed")
    print("[+] logged in as admin")


def get_token(session):
    n = nonce(session, "/settings")
    r = session.post(BASE + "/api/v1/tokens",
                     headers={"CSRF-Token": n, "Content-Type": "application/json"},
                     json={"description": "automation"})
    if r.ok and r.json().get("success"):
        return r.json()["data"]["value"]
    return None


def api(session, token, method, path, **kw):
    headers = kw.pop("headers", {})
    if token:
        headers["Authorization"] = f"Token {token}"
    headers.setdefault("Content-Type", "application/json")
    return session.request(method, BASE + "/api/v1" + path, headers=headers, **kw)


def existing_names(session, token):
    r = api(session, token, "GET", "/challenges?view=admin")
    if not r.ok:
        return set()
    return {c["name"] for c in r.json().get("data", [])}


VALUE = {"easy": 100, "medium": 250, "hard": 500, "insane": 1000}


def import_challenge(session, token, cy_path, have):
    d = cy_path.parent
    y = yaml.safe_load(cy_path.read_text())
    name = y["name"]
    if name in have:
        print(f"    = exists: {name}")
        return
    value = y.get("value") or VALUE.get(str(y.get("difficulty", "")).lower(), 100)
    payload = {
        "name": name,
        "category": y.get("category", d.parent.name),
        "description": y.get("description", ""),
        "value": int(value),
        "state": y.get("state", "visible"),
        "type": y.get("type", "standard"),
    }
    r = api(session, token, "POST", "/challenges", json=payload)
    if not r.ok or not r.json().get("success"):
        print(f"    ! failed to create {name}: {r.status_code} {r.text[:200]}")
        return
    cid = r.json()["data"]["id"]
    for fl in (y.get("flags") or []):
        content = fl["content"] if isinstance(fl, dict) else str(fl)
        api(session, token, "POST", "/flags",
            json={"challenge_id": cid, "content": content, "type": "static"})
    # files
    files = y.get("files") or []
    if files:
        fh = []
        for rel in files:
            fp = (d / rel)
            if fp.exists():
                fh.append(("file", (fp.name, fp.open("rb"))))
        if fh:
            # multipart: no JSON content-type
            api(session, token, "POST", "/files",
                headers={"Content-Type": None},
                data={"challenge_id": cid, "type": "challenge"}, files=fh)
    print(f"    + imported: {name} ({payload['category']}, {value})")


def save_config(token):
    cfgdir = ROOT / ".ctf"
    cfgdir.mkdir(exist_ok=True)
    cfg = configparser.ConfigParser()
    cfg["config"] = {"url": BASE, "access_token": token or ""}
    with open(cfgdir / "config", "w") as f:
        cfg.write(f)
    print(f"[+] wrote {cfgdir/'config'} (gitignored)")


def main():
    s = requests.Session()
    try:
        s.get(BASE, timeout=5)
    except requests.RequestException:
        raise SystemExit(f"[-] CTFd not reachable at {BASE} (is the stack up?)")
    if not is_setup(s):
        do_setup(s)
    login(s)
    token = get_token(s)
    save_config(token)
    have = existing_names(s, token)
    print("[*] importing challenges...")
    for cy in sorted(ROOT.glob("challenges/*/*/challenge.yml")):
        import_challenge(s, token, cy, have)
    print("[+] done")


if __name__ == "__main__":
    main()
