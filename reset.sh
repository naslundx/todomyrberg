docker compose down -v
docker compose up -d
docker compose exec backend uv run python setup_database.py
