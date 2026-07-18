#!/bin/bash
set -e

run_quietly() {
    local output
    if ! output=$("$@" 2>&1); then
        echo "❌ Command failed: $*"
        echo "$output"
        exit 1
    fi
}

# Frontend
cd frontend
run_quietly npm run format
run_quietly npm run type-check
run_quietly npm run lint

# Backend
cd ../backend
run_quietly uv run black --check .
run_quietly uv run pylint .
run_quietly uv run ruff check .
run_quietly uv run mypy .
