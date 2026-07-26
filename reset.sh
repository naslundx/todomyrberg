#!/usr/bin/env bash

docker compose down -v
sleep 1
docker compose up -d --build
docker compose exec backend uv run python setup_database.py
