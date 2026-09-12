# Abandoned-cart recovery voice agent

A platform-ready Bolna assignment submission for a reusable abandoned-cart recovery agent. The same prompt serves different brands and carts through `user_data`; no prompt edits are needed per call.

## Files

- `agent/prompt.txt`: paste into the Bolna agent system prompt.
- `agent/tools.json`: create these two custom tasks in Bolna and replace the two webhook URLs with your own webhook.site URLs.
- `examples/config-a.json`: Beardo, Neha, Rohan, happy-path checkout.
- `examples/config-b.json`: GIVA, Kiara, Sailaja, objections and rescheduling.
- `scripts/trigger_call.py`: sends either example to the Bolna call API.
- `scripts/validate.py`: checks placeholders, examples, and tool mappings.
- `submission/writeup.md`: short decisions and hardening write-up.

## Bolna setup

Create one outbound voice agent from scratch. Paste the prompt, then configure the two tools from `agent/tools.json`. Use the webhook.site URLs shown by your two webhook endpoints. Select the voice and LLM available in your account; the write-up records the choice and rationale.

In the dashboard Developers section, create an API key. Replace `REPLACE_WITH_BOLNA_AGENT_ID` and the recipient number in each example. Keep the API key out of the repository.

Validate locally:

```powershell
python scripts/validate.py
```

Set the key for the current PowerShell session and trigger a test call:

```powershell
$env:BOLNA_API_KEY = "your-api-key"
python scripts/trigger_call.py a
python scripts/trigger_call.py b
```

The tool calls should appear in the corresponding webhook.site request logs. Save the dashboard recordings or transcripts alongside the final submission; do not commit private phone numbers, API keys, recordings, or customer data.

## API shape

Each example follows the required request shape:

```json
{
  "agent_id": "your-agent-id",
  "recipient_phone_number": "+91XXXXXXXXXX",
  "user_data": {}
}
```

The prompt uses these exact variable names: `assistantName`, `shopName`, `customerName`, `cartDetails`, `cartPriceWords`, `discountInstruction`, `finalPriceWords`, and `checkoutLink`.
