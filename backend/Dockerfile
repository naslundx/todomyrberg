FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/

ENV UV_PROJECT_ENVIRONMENT=/opt/.venv

# Copy the dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies (without creating a virtual environment if possible, or just standard uv sync)
# RUN uv sync --frozen --no-install-project
RUN uv sync --frozen

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 5000

# Command to run the application
CMD ["uv", "run", "python", "main.py"]
