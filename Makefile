PROJECT_NAME := cnn_model

GREEN_COLOR  := \033[0;32m
RESET_COLOR  := \033[0m

install: ## install package in "editable" mode
	uv sync
	uv run pre-commit install
	@echo "Activate env with: $(GREEN_COLOR)source .venv/bin/activate$(RESET_COLOR)"

build:  ## build standalone package
	uv build

lint:  ## linting all files
	uv run pre-commit run --all-files
