"""Validate the local Bolna agent artifacts without network access."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER_PATTERN = re.compile(r"\{\{([A-Za-z][A-Za-z0-9]*)\}\}")


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    prompt = (ROOT / "agent" / "prompt.txt").read_text(encoding="utf-8")
    placeholders = set(PLACEHOLDER_PATTERN.findall(prompt))
    tool_config = load_json(ROOT / "agent" / "tools.json")
    tools = tool_config["tools"]

    assert {tool["name"] for tool in tools} == {
        "send_checkout_link",
        "reschedule_call",
    }
    for tool in tools:
        value = tool["value"]
        assert value["method"] == "POST"
        assert "webhook.site" in value["url"]
        assert set(tool["parameters"]["required"]) <= set(value["param"])

    configs = [
        load_json(ROOT / "examples" / "config-a.json"),
        load_json(ROOT / "examples" / "config-b.json"),
    ]
    for config in configs:
        missing = placeholders - set(config["user_data"])
        assert not missing, f"Missing user_data keys: {sorted(missing)}"

    assert configs[0]["user_data"]["shopName"] != configs[1]["user_data"]["shopName"]
    assert configs[0]["user_data"]["customerName"] != configs[1]["user_data"]["customerName"]
    print("Validation passed: prompt, tools, and both configurations agree.")


if __name__ == "__main__":
    main()
