# Stage 1: Build
FROM python:3.12-slim AS build
WORKDIR /app

# Install dependencies for psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim
WORKDIR /app

# Copy installed packages
COPY --from=build /install /usr/local

# Copy app code
COPY app.py .

EXPOSE 5000
CMD ["python3", "app.py"]
