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

## Test the endpoint

### Console

Endpoint → **Requests** → paste the JSON above → **Run**. The first job can take several minutes (image pull + model load + generation).

### Async API (recommended)

Image jobs often exceed `/runsync` client timeouts. Submit with `/run`, then poll `/status`.

```bash
export RUNPOD_API_KEY=your_runpod_api_key
export ENDPOINT_ID=your_endpoint_id

curl -X POST "https://api.runpod.ai/v2/${ENDPOINT_ID}/run" \
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "A cinematic photo of a golden retriever astronaut on the moon, highly detailed",
      "height": 1024,
      "width": 1024,
      "num_inference_steps": 28,
      "guidance_scale": 3.5,
      "seed": 42
    },
    "policy": {
      "executionTimeout": 900000,
      "ttl": 3600000
    }
  }'
```
