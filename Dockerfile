FROM python:3.12-slim

WORKDIR /app

COPY requirements-docker.txt .

RUN python -m pip install --upgrade pip

# Install CPU-only PyTorch.
RUN python -m pip install \
    --default-timeout=1000 \
    --retries 10 \
    --no-cache-dir \
    torch==2.13.0 \
    --index-url https://download.pytorch.org/whl/cpu

# Install the remaining QuantMind runtime dependencies.
RUN python -m pip install \
    --default-timeout=1000 \
    --retries 10 \
    --no-cache-dir \
    -r requirements-docker.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.presentation.api.app:app", "--host", "0.0.0.0", "--port", "8000"]