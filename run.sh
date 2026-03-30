#!/bin/bash
# Run script for Carousell Marketplace CLI.
# Launches the interactive REPL.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
python3 main.py
