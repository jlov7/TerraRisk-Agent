SHELL := /bin/bash

.PHONY: dev seed test chaos demo-terra backend frontend backend-test backend-lint backend-type frontend-lint eval-terra qa

dev:
	docker compose up terrarisk-backend terrarisk-frontend

seed:
	@echo "TODO: implement seed scripts for TerraRisk Agent"

test:
	cd apps/terrarisk-agent/backend && uv run pytest

chaos:
	@echo "TODO: wire chaos experiments once services mature"

backend:
	cd apps/terrarisk-agent/backend && uv run uvicorn terrarisk.main:app --reload

frontend:
	cd apps/terrarisk-agent/frontend && pnpm dev

backend-test:
	cd apps/terrarisk-agent/backend && uv run pytest

backend-lint:
	cd apps/terrarisk-agent/backend && uv run ruff check terrarisk

backend-type:
	cd apps/terrarisk-agent/backend && uv run mypy terrarisk

frontend-lint:
	cd apps/terrarisk-agent/frontend && pnpm lint

eval-terra:
	cd apps/terrarisk-agent/backend && uv run python ../evals/run_eval.py

demo-terra:
	docker compose up terrarisk-backend terrarisk-frontend opa postgres redis otel-collector

qa: backend-test backend-lint backend-type frontend-lint eval-terra
