# Source Provenance

This monorepo is a verified judge-facing source snapshot. The original repositories preserve development history; this repository is the primary entry point for review, setup, testing, and submission. No Git submodules are used.

| Component | Original repository | Verified commit | Destination |
| --- | --- | --- | --- |
| Frontend | `mahmoud-yassin10/surplus-sync-plus` | `f352cb40035043358372fd6607363b7389aa3549` | `apps/web` |
| Copilot | `mahmoud-yassin10/surplussync-copilot-lab` | `a67b766d131eed9681e6c2283938930139ae7529` | `services/copilot-api` |
| ML | `mahmoud-yassin10/surplussync-ml-service` | `8d49b87478b8ccaf82a901370c0d0db632c4cffe` | `services/ml-api` |

The imports were created from `git archive` at the exact commits above, so untracked local files, nested `.git` folders, build output, caches, virtual environments, and local secrets were not copied.
