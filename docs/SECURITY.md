# Security

## Implemented Controls

- HttpOnly assistant session cookie.
- Same-origin frontend gateways.
- Server-only service tokens.
- No client-side Gemini API key.
- Role authorization.
- Main-app reconciliation before messages and approvals.
- Stale proposal validation.
- Proposal TTL and idempotency.
- Direct API bypass protection for manual mode and partner prerequisites.
- Append-only audit behavior in the prototype store.

## Known Demo Limitations

This repository does not claim enterprise-grade authentication. The prototype does not include a production identity provider, durable enterprise database, centralized secrets manager, or production audit retention system.

## Secret Handling

Use `.env` locally and do not commit it. `.env.example` contains placeholders and local defaults only.
