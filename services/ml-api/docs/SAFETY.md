# Safety and human-in-the-loop requirements

1. **Recommendation only.** Forecast responses use `decisionStatus="PROPOSED"` and
   `approvalRequired=true`.
2. **No operational writes.** This service cannot alert partners, reserve capacity, route food,
   confirm food safety, assign drivers, or advance pickups.
3. **Preparation safety floor.** Recommendations cannot be below the configured upper uncertainty
   bound plus the operational buffer. The response discloses when the floor was applied.
4. **Canonical stability.** The recorded demo date returns the approved fixture, not an unstable
   model output.
5. **Traceability.** Every response includes model version, data quality, evidence factors, and
   generation time.
6. **What-if isolation.** Simulations do not change stored plans or records.
7. **Food safety remains human.** Recoverability and checklist decisions are outside the model.
8. **Copilot isolation.** LLM output may explain or draft, but deterministic policy checks and an
   explicit approval click remain mandatory.
