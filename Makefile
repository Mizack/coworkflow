# CoworkFlow - Makefile

.PHONY: help install test lint build up down clean test-unit test-integration test-ui test-e2e test-performance

help: ## Show this help message
	@echo "CoworkFlow - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements-test.txt
	@echo "Dependencies installed successfully"

test: ## Run all tests
	@echo "Running all tests..."
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing

test-unit: ## Run unit tests only
	@echo "Running unit tests..."
	pytest tests/unit/ -v --cov=. --cov-report=html

test-integration: ## Run integration tests
	@echo "Starting services for integration tests..."
	docker-compose up -d
	sleep 30
	pytest tests/integration/ -v
	docker-compose down

test-ui: ## Run UI tests
	@echo "Starting services for UI tests..."
	docker-compose up -d
	sleep 45
	pytest tests/ui/ -v --tb=short
	docker-compose down

test-e2e: ## Run E2E tests
	@echo "Starting all services for E2E tests..."
	docker-compose up -d
	sleep 60
	pytest tests/e2e/ -v --tb=short
	docker-compose down

test-performance: ## Run performance tests
	@echo "Starting services for performance tests..."
	docker-compose up -d
	sleep 30
	locust -f tests/performance/load_test.py --host=http://localhost:8000 --users=10 --spawn-rate=2 --run-time=60s --headless
	docker-compose down

lint: ## Run code linting
	@echo "Running flake8 linting..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

build: ## Build all Docker images
	@echo "Building Docker images..."
	docker-compose build

up: ## Start all services
	@echo "Starting CoworkFlow services..."
	docker-compose up -d
	@echo "Services started. Frontend: http://localhost:3000, API: http://localhost:8000"

down: ## Stop all services
	@echo "Stopping CoworkFlow services..."
	docker-compose down

clean: ## Clean Docker resources
	@echo "Cleaning Docker resources..."
	docker-compose down -v --remove-orphans
	docker system prune -f

coverage: ## Generate coverage report
	pytest tests/unit/ --cov=. --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

quick-test: ## Quick test run (unit tests only)
	pytest tests/unit/ -x -v