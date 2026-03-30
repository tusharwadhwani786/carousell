#!/bin/bash
# Build script for Carousell Marketplace CLI.
# Validates Python 3 availability and runs a syntax check on all source files.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Carousell Marketplace CLI - Build ==="

if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is not installed or not in PATH"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo "Using: $PYTHON_VERSION"

echo "Running syntax check..."
python3 -m py_compile main.py

find marketplace -name '*.py' -print0 | while IFS= read -r -d '' f; do
    python3 -m py_compile "$f"
done

echo "Syntax check passed."

echo "=== Build complete ==="
