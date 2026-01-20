# Use a lightweight Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set the working directory
WORKDIR /app

# Enable bytecode compilation and intermediate layers for faster builds
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies first (better for caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of the app (including your ONNX files)
COPY . /app

# Sync the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place the virtual environment at the front of the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose ports for both FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# For a single-container deployment, we'll use a script to start both
# CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]