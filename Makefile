.PHONY: build run test clean lint

build:
	@bash ./build.sh

run:
	@bash ./run.sh

test:
	@echo "=== Running tests ==="
	@python3 -m unittest discover -s tests -v
	@echo "=== All tests passed ==="

clean:
	@echo "Cleaning up..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "Clean complete."

lint:
	@echo "=== Running syntax check ==="
	@python3 -m py_compile main.py
	@find marketplace -name '*.py' -print0 | while IFS= read -r -d '' f; do python3 -m py_compile "$$f"; done
	@echo "Syntax check passed."
