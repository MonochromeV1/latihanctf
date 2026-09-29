"""Pluggable LLM backend for the AI challenges.

LLM_BACKEND selects the backend (default: mock — deterministic, offline, no key):
  - mock    : a deterministic "gullible assistant" that simulates an LLM which
              knows the system prompt (including the flag) and complies with
              jailbreaks / encoding / injection requests. Makes every challenge
              solvable and testable with no API key or GPU.
  - ollama  : POST to {LLM_API_BASE}/api/chat  (LLM_MODEL, e.g. llama3)
  - openai  : POST to {LLM_API_BASE}/chat/completions  (LLM_MODEL, LLM_API_KEY)

The per-tier DEFENSES (input/output guardrails, judge) live in each app.py, not
here — this module only produces a model reply.
"""
import base64
import codecs
import os
import re

import requests

JAILBREAK = ["pretend", "roleplay", "role play", "role-play", "act as", "you are now",
             "dan", "ignore previous", "ignore all", "story", "game", "hypothetical",
             "opposite day", "developer mode", "debug", "as an admin", "grandma",
             "simulate", "no rules"]


def _flag(system):
    m = re.search(r"claude\{[^}]+\}", system)
    return m.group(0) if m else ""


def _enc_req(u):
    if "base64" in u or "b64" in u:
        return "base64"
    if "rot13" in u:
        return "rot13"
    if ("hyphen" in u or "dash" in u or "spell" in u or "between each" in u
            or ("separate" in u and "char" in u)):
        return "hyphen"
    if "reverse" in u or "backwards" in u:
        return "reverse"
    return None


def _produce(flag, enc):
    if enc == "base64":
        return base64.b64encode(flag.encode()).decode()
    if enc == "rot13":
        return codecs.encode(flag, "rot_13")
    if enc == "hyphen":
        return "-".join(flag)
    if enc == "reverse":
        return flag[::-1]
    return flag


def mock_reply(system, user):
    flag = _flag(system)
    u = user.lower()
    s = system.lower()
    guard = ("never reveal" in s) or ("do not reveal" in s) or ("don't reveal" in s)
    enc = _enc_req(u)
    jb = any(k in u for k in JAILBREAK)
    asks = any(k in u for k in ["flag", "secret", "password", "the key", "claude{"])
    inject = (("append" in u or "also output" in u or "after summar" in u
               or "ignore" in u or "instruction" in u or "at the end" in u) and asks)
    if not guard:
        if asks or enc:
            return "The secret is: " + _produce(flag, enc)
        return "Hi! I'm a friendly assistant. Ask me anything."
    if jb or enc or inject:
        return "Okay, as requested: " + _produce(flag, enc)
    if asks:
        return "I'm sorry, but I can't reveal the secret."
    return "Hello! How can I help you today?"


def call_llm(system, user):
    backend = os.environ.get("LLM_BACKEND", "mock").lower()
    if backend == "mock" or not backend:
        return mock_reply(system, user)
    try:
        if backend == "ollama":
            base = os.environ.get("LLM_API_BASE", "http://host.docker.internal:11434").rstrip("/")
            model = os.environ.get("LLM_MODEL", "llama3")
            r = requests.post(base + "/api/chat", timeout=120, json={
                "model": model, "stream": False,
                "messages": [{"role": "system", "content": system},
                             {"role": "user", "content": user}]})
            return r.json().get("message", {}).get("content", "")
        if backend in ("openai", "api"):
            base = os.environ.get("LLM_API_BASE", "https://api.openai.com/v1").rstrip("/")
            model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
            key = os.environ.get("LLM_API_KEY", "")
            r = requests.post(base + "/chat/completions", timeout=120,
                              headers={"Authorization": f"Bearer {key}"},
                              json={"model": model, "messages": [
                                  {"role": "system", "content": system},
                                  {"role": "user", "content": user}]})
            return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[backend error: {e}]"
    return mock_reply(system, user)
