# Demo Guide

## Canonical Scenario

- School: Lincoln Heights Public High School
- Date: Thursday, 2026-03-12
- Normal prep: 730
- Baseline attendance: 528
- Interval: 497-557
- Recommended prep: 562
- Preventable surplus: 168
- Shortage probability: 4.1%
- Corrected attendance: 540
- Corrected interval: 512-568
- Corrected prep: 575
- Corrected preventable surplus: 155
- Safety floor: 540
- Safety buffer: 7

## Role

Use an authorized cafeteria or admin role for approvals. Use strict manual mode to show blocked execution.

## Sequence and Expected States

1. Open Command Center and confirm high-risk Thursday.
2. Inspect the uncertainty interval and recommendation.
3. Open evidence to see trips, early dismissal, exams, rain, menu, and attendance trend.
4. Ask why Thursday is high risk. Expected answer references the canonical forecast and uncertainty.
5. Run field-trip cancellation simulation. Expected result: attendance 540 and prep 575.
6. Confirm simulation does not mutate state until approval.
7. Create and approve attendance proposal.
8. Review corrected recommendation.
9. Attempt partner selection before surplus/checklist prerequisites. Expected result: blocked.
10. Complete surplus confirmation and checklist.
11. Approve eligible partner selection.
12. Review impact ledger and audit history.
13. Enable strict manual mode and confirm execution is blocked.
14. Reset demo.

## Troubleshooting

- If Gemini is unavailable, continue with deterministic fallback.
- If Copilot session is stale, reset the assistant session or run the demo reset.
- If the map does not load, switch to schematic map.
- If Vite chose a different port, use the printed frontend URL.
