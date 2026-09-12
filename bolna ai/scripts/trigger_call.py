"""Trigger a Bolna call from one of the checked-in example payloads."""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"a", "b"}:
        raise SystemExit("Usage: python scripts/trigger_call.py a|b")

    api_key = os.environ.get("BOLNA_API_KEY")
    if not api_key:
        raise SystemExit("Set BOLNA_API_KEY before triggering a call.")

    config_path = ROOT / "examples" / f"config-{sys.argv[1]}.json"
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    request = urllib.request.Request(
        "https://api.bolna.ai/call",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            print(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Bolna rejected the request ({error.code}): {body}") from error


if __name__ == "__main__":
    main()
