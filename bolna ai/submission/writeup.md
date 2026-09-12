# Abandoned-cart recovery agent write-up

## Decisions

I used one generic prompt with per-call `user_data`, so brand, persona, customer, cart, price, discount, final price, and checkout URL never require prompt edits. Prices arrive pre-worded and the agent is explicitly forbidden from arithmetic or digit-to-word conversion.

The flow is deliberately short: identity confirmation, one opening pitch, reason probing, one concise objection response, discount nudge when available, and a tool-backed close. The prompt keeps turns to two sentences, asks one question at a time, preserves the current language, and uses Devanagari for Hindi. It also tells the agent to end on wrong numbers, after two failed identity attempts, or after a tool failure without pretending success.

I chose the clearest female voice and a fast general-purpose LLM available in the Bolna account. A warm female voice matches the `Neha` and `Kiara` personas; the LLM is instructed to prioritize the compact turn budget and supplied facts over improvisation.

The two custom tasks are `send_checkout_link` and `reschedule_call`. Each has a filler message, a strict JSON schema, a POST method, and a webhook.site endpoint. Checkout requires clear purchase agreement. Rescheduling requires both a date and time from the customer before invocation.

## Test evidence to attach

Config A should be a happy path for Beardo and Rohan, ending with the checkout webhook receiving the cart, final price, and checkout URL. Config B should use GIVA and Sailaja, include at least two objections, request a callback, and show the reschedule webhook receiving the chosen date and time. Attach the two dashboard transcripts or recordings and the two webhook request logs.

## What broke during testing

Record the actual issues found here after the calls, such as pronunciation of product names, overly long turns, accidental language switching, or a tool firing before confirmation. The repository includes a local validator for static configuration issues, but live call quality still needs transcript review.

## Million-calls-per-week hardening

I would add webhook authentication and retries with idempotency keys, queue-based call scheduling, rate limits, opt-out and consent enforcement, timezone-aware callback storage, and structured tool error handling. I would also add automated transcript evaluations for identity confirmation, language and script compliance, digit leaks, discount accuracy, tool timing, and the exact-one closing question. Finally, I would monitor latency, answer rate, conversion, opt-outs, failed webhooks, and per-brand regressions with redacted logs and sampled recordings.
