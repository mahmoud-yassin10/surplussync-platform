# Responsible AI

## Human Oversight

The AI assistant explains, simulates, and proposes. Authorized humans approve consequential actions.

## Uncertainty

Forecasts include intervals and safety buffers. The UI avoids presenting recommendations as certainties.

## Privacy

The prototype uses synthetic aggregate data and no private student-level records.

## Fairness

The system should be evaluated with real deployment data before use in diverse schools. It must not be used to deny meals or reduce service access.

## Explainability

Forecast evidence, similar days, what-if results, and proposal consequences are shown to users.

## Manual Mode

Strict manual mode blocks executable proposals and approval execution. Old proposals do not automatically revive when mode changes.

## Permissions and Server Checks

Role permissions, proposal freshness, partner prerequisites, stale sessions, and direct API bypass protections are enforced server-side.

## Prohibited Autonomous Actions

The AI cannot contact partners, reserve capacity, schedule pickups, approve itself, delete audit history, bypass food-safety checks, or execute irreversible actions.

## Deployment Limitations

This is a hackathon prototype, not a production deployment. Production use would require identity management, durable audit storage, monitoring, real data validation, and local policy review.
