.PHONY: setup install clean coordinator

setup:
	@echo "Creating virtual environment with uv..."
	uv venv --python 3.12
	@echo "Virtual environment created at .venv"
	@echo "Run: source .venv/bin/activate"

install:
	@echo "Installing root package..."
	uv pip install -e .
	@echo "Installing coordinator service..."
	uv pip install -e services/coordinator/
	@echo "Installing github service..."
	uv pip install -e services/github/
	@echo "All packages installed successfully!"

clean:
	@echo "Removing virtual environment..."
	rm -rf .venv
	@echo "Removing build artifacts..."
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	@echo "Clean complete."

coordinator:
	@echo "Running Coordinator Node..."
	.venv/bin/python3 -m services.coordinator.node

github:
	@echo "Running Github Node..."
	.venv/bin/python3 -m services.github.node