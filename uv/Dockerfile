FROM alpine:3.22

RUN apk add --no-cache curl

ENV XDG_BIN_HOME=/usr/local/bin
ENV UV_NO_MODIFY_PATH=1
RUN curl -LsSf https://astral.sh/uv/0.7.19/install.sh | sh

WORKDIR /app
COPY . /app

ENV UV_CACHE_DIR="/app/.cache/uv"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=ssh \
    --mount=type=cache,target=/app/.cache/uv \
    /usr/local/bin/uv lock --locked && uv sync --no-dev

EXPOSE 8080/tcp
ENTRYPOINT ["/app/.venv/bin/python", "-m", "custom_predictor", "serve"]
