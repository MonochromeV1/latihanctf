SHELL := /bin/bash
VENV  := .venv
PY    := $(VENV)/bin/python
COMPOSE := docker compose

.DEFAULT_GOAL := help

.PHONY: help venv build up down deploy test clean prune status

help:
	@echo "LatihanCTF — targets:"
	@echo "  make venv     - create solver virtualenv (.venv)"
	@echo "  make build    - build all challenge docker images"
	@echo "  make up       - start CTFd + all networked challenges"
	@echo "  make deploy   - up + import challenges into CTFd"
	@echo "  make test     - run every automated solver, assert real flag / no decoy"
	@echo "  make down     - stop the stack"
	@echo "  make clean    - stop stack + remove volumes"
	@echo "  make status   - show running containers"

venv:
	python3 -m venv $(VENV)
	$(PY) -m pip install -q --upgrade pip wheel
	$(PY) -m pip install -q requests pycryptodome Pillow sympy z3-solver ctfcli

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d
	@echo "CTFd: http://127.0.0.1:8000"

down:
	$(COMPOSE) down

deploy: up
	@echo "[*] waiting for CTFd..."; sleep 8
	$(PY) scripts/setup_ctfd.py

test:
	$(PY) scripts/run_solvers.py $(FILTER)

status:
	$(COMPOSE) ps

clean:
	$(COMPOSE) down -v || true

prune: clean
	docker system prune -f
