
### 7.4 Root `Makefile`

```makefile
# ============================================================
# BusGo — Makefile
# ============================================================

.PHONY: help install dev test lint format clean docker-up docker-down docker-logs

# ---------- Help ----------
help:
	@echo "BusGo — available commands:"
	@echo "  make install         Install all dependencies"
	@echo "  make dev             Start development environment"
	@echo "  make test            Run all tests"
	@echo "  make lint            Run linters"
	@echo "  make format          Format code"
	@echo "  make clean           Clean caches"
	@echo "  make docker-up       Start Docker Compose"
	@echo "  make docker-down     Stop Docker Compose"
	@echo "  make docker-logs     View logs"

# ---------- Install ----------
install:
	@echo "Installing identity-service dependencies..."
	cd services/identity-service && pip install -r requirements/development.txt
	@echo "Installing FastAPI services dependencies..."
	@for s in bus booking payment notification; do \
		cd services/$$s-service && pip install -r requirements/development.txt && cd ../../; \
	done

# ---------- Dev ----------
dev:
	@echo "Starting development environment..."
	docker compose up -d postgres redis

# ---------- Test ----------
test:
	@for s in identity bus booking payment notification; do \
		cd services/$$s-service && pytest -v && cd ../../; \
	done

# ---------- Lint ----------
lint:
	@for s in identity bus booking payment notification; do \
		cd services/$$s-service && ruff check . && cd ../../; \
	done

# ---------- Format ----------
format:
	@for s in identity bus booking payment notification; do \
		cd services/$$s-service && ruff format . && cd ../../; \
	done

# ---------- Clean ----------
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# ---------- Docker ----------
docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f