FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY auto_setup_llama.py .

RUN python3 auto_setup_llama.py

RUN mkdir -p models

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

ENV MODEL_PATH="models/phi-4-mini-instruct-q4_k_m.gguf"
ENV HOST="0.0.0.0"
ENV PORT="8080"
ENV CONTEXT_SIZE="4096"
ENV THREADS="8"
ENV GPU_LAYERS="0"

CMD ./server \
    -m "$MODEL_PATH" \
    --host "$HOST" \
    --port "$PORT" \
    -c "$CONTEXT_SIZE" \
    -t "$THREADS" \
    --n-gpu-layers "$GPU_LAYERS"