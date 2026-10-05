import os
import sys

from huggingface_hub import snapshot_download

MODEL_ID = "black-forest-labs/FLUX.1-dev"


def main() -> None:
    token = os.environ.get("HF_TOKEN")
    if not token:
        print(
            "HF_TOKEN is missing. Rebuild with:\n"
            "  docker build --platform linux/amd64 "
            "--build-arg HF_TOKEN=$HF_TOKEN "
            "--tag YOUR_DOCKERHUB_USER/flux-dev-serverless:latest ."
        )
        sys.exit(1)

    # Cache files only. Do not call FluxPipeline.from_pretrained() here —
    # that loads ~24GB+ into RAM and fails inside Docker Desktop.
    snapshot_download(
        repo_id=MODEL_ID,
        token=token,
        resume_download=True,
    )
    print(f"{MODEL_ID} cached successfully")


if __name__ == "__main__":
    main()
