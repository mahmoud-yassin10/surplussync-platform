# Security

## Implemented Controls

- HttpOnly assistant session cookie.
- Same-origin frontend gateways.
- Server-only service tokens.
- No client-side Gemini API key.
- Optional Upstash Redis persistence for Copilot sessions.
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

The frontend server gateway sends `COPILOT_SERVICE_TOKEN` as a bearer token to the Copilot API. That value must match the Copilot service's `MAIN_APP_SERVICE_TOKEN`. Redis and Gemini secrets belong only in the Copilot Vercel project environment. No Redis, Gemini, or service-token secret should use a `VITE_` prefix or be exposed to browser bundles.

When Redis variables are absent, Copilot sessions use in-memory fallback. This is acceptable for local development and CI, but Vercel deployments should configure Upstash Redis so sessions survive serverless instance changes.
