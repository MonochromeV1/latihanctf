# Read the Fine Metadata — writeup

**Real flag:** `claude{doc_metadata_led_to_the_mirror}`.

## Solve
`brief.docx` is a zip; read `docProps/core.xml`. Its `<cp:keywords>` leaks
`mirror path: notes/brief_9f2a1c.html`. That page exists in the mirror but is not
linked from `index.html`; open it for the flag.

```bash
unzip -p brief.docx docProps/core.xml   # see the keywords
CHALLENGE_DIST=../dist python3 solve.py
```

## Planted decoys (NOT accepted)
| Decoy | Location |
|-------|----------|
| `claude{document_body_text_decoy}` | docx body text |
| `claude{mirror_index_decoy}` | mirror `index.html` comment |
