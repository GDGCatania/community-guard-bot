# Build
FROM python:3.13-slim AS build

WORKDIR /app

RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir aiohttp

# Prod
FROM python:3.13-slim AS production

WORKDIR /app

COPY --from=build /app/venv /app/venv
COPY . .

EXPOSE 8080

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
