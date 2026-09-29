# Same Handle, Different Person — writeup

**Real flag:** `claude{username_pivot_to_the_paste}`.

## Solve
Start at `profiles/devforum.html` (the real n0cturnal_dev). Its bio links the
account's paste dump `paste_n0cturnal.html`, which holds the flag. The microblog
account only *reuses* the handle (different join date) and posts a fake flag.

```bash
CHALLENGE_DIST=../dist python3 solve.py
```

## Planted decoys (NOT accepted)
| Decoy | Location |
|-------|----------|
| `claude{same_username_different_person}` | lookalike microblog bio |
| `claude{devforum_draft_comment_decoy}` | HTML comment on devforum profile |
