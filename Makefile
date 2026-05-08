PROJECT_NAME := neur

GREEN_COLOR  := \033[0;32m
RESET_COLOR  := \033[0m

install: ## install package in "editable" mode
	uv sync
	@echo "Activate env with: $(GREEN_COLOR)source .venv/bin/activate$(RESET_COLOR)"

install-dev: install ## install package in "editable" mode
	uv sync --dev
	uv run pre-commit install
	@echo "Activate env with: $(GREEN_COLOR)source .venv/bin/activate$(RESET_COLOR)"

build:  ## build standalone package
	uv build

lint:  ## linting all files
	uv run pre-commit run --all-files
