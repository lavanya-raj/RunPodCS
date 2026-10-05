# RunPod Case Study 

| File | Role |
|---|---|
| `handler.py` | Runpod Serverless handler: load pipeline once, generate image, return base64 |
| `download_weights.py` | Caches FLUX.1-dev into `HF_HOME` during the image build |
| `Dockerfile` | CUDA 12.1 + Python 3.11 venv + Torch + handler + baked model cache |
| `requirements.txt` | Python deps (`runpod`, `diffusers`, `transformers`, …)|

## Build and push the image

# Export token
export HF_TOKEN=hf_your_token_here
export DOCKER_USER=your_dockerhub_username

echo "${HF_TOKEN:+HF_TOKEN is set}"

# Build Docker
docker build --platform linux/amd64 \
  --build-arg HF_TOKEN="$HF_TOKEN" \
  --tag $DOCKER_USER/flux-dev-serverless:latest .

docker login
docker push $DOCKER_USER/flux-dev-serverless:latest


`--platform linux/amd64` is required for Runpod.
`--build-arg HF_TOKEN` is required because the repo is gated. The token is used only for that download `RUN` and is not stored as a container `ENV`.
