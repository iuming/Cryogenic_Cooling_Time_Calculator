.PHONY: help install test format lint clean run docs build
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -e ".[dev]"

install-prod: ## Install production dependencies only
	pip install -r requirements.txt

test: ## Run tests
	python -m pytest tests/ scripts/ utils/ -v

test-coverage: ## Run tests with coverage
	python -m pytest tests/ scripts/ utils/ --cov=core --cov=utils --cov-report=html

format: ## Format code with black and isort
	black .
	isort .

lint: ## Run linting with flake8
	flake8 .

type-check: ## Run type checking with mypy (if available)
	@command -v mypy >/dev/null 2>&1 && mypy . || echo "mypy not installed, skipping type check"

clean: ## Clean up cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/

run: ## Run the application
	python cooling_gui.py

run-simple: ## Run simple calculator
	python scripts/simple_calculator.py

docs: ## Build documentation (if available)
	@command -v sphinx-build >/dev/null 2>&1 && sphinx-build -b html docs_source docs_build || echo "Sphinx not available"

build: ## Build package
	python -m build

check: format lint test ## Run all checks (format, lint, test)

setup-dev: install ## Setup development environment
	@echo "Development environment setup complete!"
	@echo "Run 'make run' to start the application"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make check' to run all quality checks"

# Windows-specific targets
install-win: ## Install dependencies on Windows
	python -m pip install -e ".[dev]"

run-win: ## Run application on Windows
	python cooling_gui.py

clean-win: ## Clean up on Windows
	if exist __pycache__ rmdir /s /q __pycache__
	if exist build rmdir /s /q build
	if exist dist rmdir /s /q dist
	for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
