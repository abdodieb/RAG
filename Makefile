.PHONY: help up down build restart logs clean ps shell-api shell-airflow health status stop start install dev-install run-local

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the project as a package
	pip install -e .

dev-install: ## Install the project with development dependencies
	pip install -e ".[dev]"

run-local: ## Run the API locally (without Docker)
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

up: ## Start all services (docker compose up -d)
	docker compose up -d

down: ## Stop and remove all containers (docker compose down)
	docker compose down

build: ## Build all images (docker compose build)
	docker compose build

rebuild: ## Rebuild and restart all services
	docker compose down
	docker compose build --no-cache
	docker compose up -d

restart: ## Restart all services
	docker compose restart

logs: ## Show logs from all services (docker compose logs -f)
	docker compose logs -f

logs-api: ## Show logs from API service only
	docker compose logs -f api

logs-airflow: ## Show logs from Airflow service only
	docker compose logs -f airflow

logs-ollama: ## Show logs from Ollama service only
	docker compose logs -f ollama

ps: ## List all running containers (docker compose ps)
	docker compose ps

stop: ## Stop all services without removing containers
	docker compose stop

start: ## Start existing containers
	docker compose start

clean: ## Stop and remove all containers, networks, and volumes
	docker compose down -v

clean-build: ## Remove all containers, volumes, and rebuild from scratch
	docker compose down -v
	docker compose build --no-cache
	docker compose up -d

shell-api: ## Open shell in API container
	docker compose exec api /bin/bash

shell-airflow: ## Open shell in Airflow container
	docker compose exec airflow /bin/bash

shell-postgres: ## Open PostgreSQL shell
	docker compose exec postgres psql -U rag_user -d rag_db

shell-opensearch: ## Open shell in OpenSearch container
	docker compose exec opensearch /bin/bash

health: ## Check health status of all services
	docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

status: ## Show detailed status of all services
	@echo "=== Service Status ==="
	@docker compose ps
	@echo ""
	@echo "=== Volume Usage ==="
	@docker volume ls | grep rag

pull: ## Pull latest images
	docker compose pull

update: ## Pull latest images and restart services
	docker compose pull
	docker compose up -d

exec-api: ## Execute command in API container (usage: make exec-api CMD="ls -la")
	docker compose exec api $(CMD)

exec-airflow: ## Execute command in Airflow container (usage: make exec-airflow CMD="ls -la")
	docker compose exec airflow $(CMD)

reset-db: ## Reset PostgreSQL database (WARNING: deletes all data)
	docker compose stop postgres
	docker volume rm rag_postgres_data
	docker compose up -d postgres

reset-opensearch: ## Reset OpenSearch data (WARNING: deletes all indices)
	docker compose stop opensearch
	docker volume rm rag_opensearch_data
	docker compose up -d opensearch

reset-all: ## Reset everything (WARNING: deletes all data)
	docker compose down -v
	docker compose up -d

dev: ## Start in development mode with logs
	docker compose up

prod: ## Start in production mode (detached)
	docker compose up -d

watch: ## Watch service logs in real-time
	docker compose logs -f --tail=100
