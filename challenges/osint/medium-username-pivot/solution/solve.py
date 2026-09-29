#!/usr/bin/env python3
"""OSINT/Medium solver — start at the primary profile, pivot via the linked paste
(the real account), and read the flag there. Ignores the lookalike/microblog and
draft-comment decoys."""
import os
import re
import sys

DIST = os.environ.get("CHALLENGE_DIST",
                      os.path.join(os.path.dirname(__file__), "..", "dist"))
PROFILES = os.path.join(DIST, "profiles")
DECOYS = {"claude{same_username_different_person}",
          "claude{devforum_draft_comment_decoy}"}


def main():
    primary = open(os.path.join(PROFILES, "devforum.html")).read()
    # pivot: the primary profile links its real paste dump
    m = re.search(r'href="(paste_[^"]+\.html)"', primary)
    if not m:
        print("no pivot link found", file=sys.stderr)
        sys.exit(1)
    paste = open(os.path.join(PROFILES, m.group(1))).read()
    for f in re.findall(r"claude\{[^}]+\}", paste):
        if f not in DECOYS:
            print(f)
            return
    print("no flag on pivoted page", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
