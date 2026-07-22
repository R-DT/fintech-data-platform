# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /build

# Install system dependencies required to compile database drivers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Final minimal runtime image
FROM python:3.11-slim AS runner

WORKDIR /app

# Install runtime PostgreSQL client library dependency
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed dependencies from builder stage
COPY --from=builder /root/.local /root/.local
COPY src/ ./src/
COPY pyproject.toml .
COPY README.md .

ENV PATH=/root/.local/bin:$PATH

# Install the package in development mode inside the container
RUN pip install --no-cache-dir -e .

ENTRYPOINT ["fintech-platform"]
