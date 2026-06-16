.PHONY: install dev test clean lint

install:
	pip install -r requirements.txt

dev:
	uvicorn src.api.main:app --reload --port 8000

test:
	pytest tests/ -v

lint:
	ruff check src/
	black --check src/

format:
	black src/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
