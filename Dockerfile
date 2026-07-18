# Stage 1: Build the frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend

# Prevent Node from using too much RAM on Raspberry Pi
ENV NODE_OPTIONS="--max-old-space-size=512"

# Install dependencies and build
COPY frontend/package*.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the backend and serve the app
FROM python:3.13-slim
WORKDIR /app/backend

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/
ENV UV_PROJECT_ENVIRONMENT=/opt/.venv

# Copy backend dependencies and install
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen

# Copy backend source code
COPY backend/ ./

# Copy the built frontend from Stage 1
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Expose port and run Gunicorn
EXPOSE 5000
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
