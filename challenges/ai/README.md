# AI / Prompt-Injection challenges

Each challenge is a small chat app whose LLM backend is **pluggable** via env vars.
It defaults to a deterministic **mock** backend so every challenge is solvable and
testable with **no API key and no GPU**.

```bash
# default: offline deterministic mock
LLM_BACKEND=mock

# local Ollama
LLM_BACKEND=ollama LLM_MODEL=llama3 LLM_API_BASE=http://host.docker.internal:11434

# OpenAI-compatible API
LLM_BACKEND=openai LLM_MODEL=gpt-4o-mini LLM_API_BASE=https://api.openai.com/v1 LLM_API_KEY=sk-...
```

Set these in the environment before `docker compose up` (the compose file passes
them through to the `ai-*` services). See `easy-system-prompt/src/llm.py`.

## The mock backend

`llm.py`'s mock simulates a *gullible* assistant that knows its system prompt
(which contains the flag) and complies with jailbreak / encoding / injection
requests, while refusing naive direct asks when the system prompt says so. The
per-tier **defenses** (input guardrail, output filter, judge, RAG path) are
implemented in each `app.py` around the model call — exactly where real guardrails
live — so the intended bypass is what actually beats them.

With a real backend (Ollama/API) the same apps work, but success depends on the
model actually following the prompt/injection; the mock guarantees a deterministic,
gradeable challenge.

| Tier | Defense | Intended bypass |
|------|---------|-----------------|
| Easy | none | just ask |
| Medium | refuses direct asks | roleplay / jailbreak framing |
| Hard | output filter redacts literal flag | make it emit the flag base64-encoded, decode |
| Insane | input+output guardrails + judge | indirect injection via `/summarize` (RAG) + a novel (hyphen) encoding |
