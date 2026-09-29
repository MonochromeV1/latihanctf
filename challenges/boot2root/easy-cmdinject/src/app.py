#!/usr/bin/env python3
"""Boot2Root / Easy — "NetTools" web app with a command-injection foothold.
Runs as the low-priv user `webadmin`. The ping host field is passed to a shell
unsanitized → RCE as webadmin. From there: read user.txt, then privesc via a
sudo/find (GTFOBins) misconfiguration to read root.txt."""
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return ("<h1>NetTools</h1>"
            "<p>Diagnostics console.</p>"
            "<form action='/ping'><input name='host' placeholder='host'>"
            "<button>ping</button></form>")


@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    # INTENTIONALLY VULNERABLE: unsanitized input into a shell.
    out = subprocess.run("ping -c 1 " + host, shell=True,
                         capture_output=True, text=True, timeout=20)
    return "<pre>" + out.stdout + out.stderr + "</pre>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
