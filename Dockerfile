FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /usr/src/app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /usr/src/app
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-install-project --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/usr/src/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []


FROM builder AS dev
WORKDIR /usr/src/app
RUN uv sync --all-extras
COPY . /usr/src/app
COPY --chmod=755 ./bin/server ./bin/server

EXPOSE 8080

CMD ["/usr/src/app/bin/server"]
