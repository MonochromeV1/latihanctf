Boot2Root: "NetTools" box — http://127.0.0.1:9001/

Goal: land TWO flags.
  user.txt  → /home/<user>/user.txt  (this challenge)
  root.txt  → /root/root.txt         (the "…: root" challenge)

Foothold: the diagnostics page runs your input through a shell. Get a shell as the
low-priv user, grab user.txt, then escalate. Decoy user.txt files are scattered in
web roots and /tmp — those are NOT accepted.
