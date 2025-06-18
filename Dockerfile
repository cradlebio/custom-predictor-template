FROM ghcr.io/astral-sh/uv:0.7.13-alpine3.21

WORKDIR /app
COPY . /app

ENV UV_CACHE_DIR="/app/.cache/uv"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=ssh \
    --mount=type=cache,target=/app/.cache/uv \
    uv lock --locked && uv sync --no-dev

EXPOSE 8080/tcp
ENTRYPOINT ["/app/.venv/bin/server"]
