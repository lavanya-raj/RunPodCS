import os
import json
import base64
import requests

endpoint_id = os.environ["ENDPOINT_ID"]
api_key = os.environ["RUNPOD_API_KEY"]

script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir, "test_input.json"), encoding="utf-8") as f:
    payload = json.load(f)
# test_input.json is already {"input": {...}}. Do not wrap it again.
if "input" not in payload:
    payload = {"input": payload}

resp = requests.post(
    f"https://api.runpod.ai/v2/{endpoint_id}/runsync",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json=payload,
    timeout=900,
)
resp.raise_for_status()
data = resp.json()

print(json.dumps({k: data[k] for k in data if k != "output"}, indent=2))

if data.get("status") != "COMPLETED" or "output" not in data:
    print("Job did not complete. Full response:")
    print(json.dumps(data, indent=2)[:4000])
    raise SystemExit(1)

output = data["output"]
# handler.py returns {"image_base64": "..."}, not {"image": "..."}
image_field = output.get("image_base64") or output.get("image")
if not image_field:
    print("No image in output. Full output keys:", list(output.keys()) if isinstance(output, dict) else type(output))
    print(json.dumps(output, indent=2)[:2000])
    raise SystemExit(1)

b64 = image_field.split(",", 1)[1] if image_field.startswith("data:") else image_field
with open("flux_woman_output.png", "wb") as f:
    f.write(base64.b64decode(b64))
print("Saved flux_woman_output.png")
