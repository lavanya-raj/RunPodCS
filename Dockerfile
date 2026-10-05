FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/root/.cache/huggingface
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN python3.11 -m venv /opt/venv

WORKDIR /

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cu121 \
    && pip install --no-cache-dir -r /requirements.txt

COPY download_weights.py handler.py /

# Token is only needed while caching the gated repo. Do not persist it as ENV.
ARG HF_TOKEN
RUN test -n "$HF_TOKEN" || (echo "HF_TOKEN build-arg is empty" && exit 1)
RUN HF_TOKEN=$HF_TOKEN python /download_weights.py

CMD ["python", "-u", "/handler.py"]
