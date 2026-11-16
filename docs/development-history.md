# GOOD NEIGHBOURS — Development History

> A transparent development record for reassessment. This document describes the project lifecycle and links each completed phase to real repository evidence. It does not rewrite or replace Git history.

## Project lifecycle

```text
01  Project Initiation
        ↓
02  Requirement Analysis
        ↓
03  System Design
        ↓
04  Initial Project Setup
        ↓
05  Core Game Development
        ↓
06  NPC & Quest Implementation
        ↓
07  UI & Asset Integration
        ↓
08  Testing & Debugging
        ↓
09  Documentation
        ↓
10  Final Release
```

## Phase record

| No. | Phase | Status | Evidence |
| --- | --- | --- | --- |
| 01 | Project Initiation | Complete | Project title, creative identity, and scope in [`GOOD_NEIGHBOURS_MASTERFILE.md`](../GOOD_NEIGHBOURS_MASTERFILE.md). |
| 02 | Requirement Analysis | Complete | Challenge requirements, controls, scoring, victory, game-over, and QA requirements recorded in the masterfile. |
| 03 | System Design | Complete | State-driven Pygame architecture, world interactions, inventory, missions, interiors, and audio flow documented in [`architecture.md`](architecture.md). |
| 04 | Initial Project Setup | Complete | Root executable `game.py`, dependency declarations, `.gitignore`, asset directory, screenshots, and README. |
| 05 | Core Game Development | Complete | Delta-time movement, collision, timed afternoon, map rendering, indoor movement, game states, restart, victory, and game-over handling. |
| 06 | NPC & Quest Implementation | Complete | Deepak, Madhu, Dhinesh, and Nethra; three one-time delivery quests; Community Trust; guided objectives; portrait dialogue. |
| 07 | UI & Asset Integration | Complete | Generated map, building interiors, item sprites, resident portraits, loading logo, animated pickups, dynamic inventory, settings, credits, music, and victory gathering. |
| 08 | Testing & Debugging | Complete | Headless automated quest tests and a full fresh-playthrough regression test in [`tests/`](../tests/). |
| 09 | Documentation | Complete | README, architecture notes, roadmap, evaluation checklist, screenshots, and this traceable lifecycle record. |
| 10 | Final Release | Pending review | Development branch is pushed and ready for reviewer approval. Release tagging should occur only after pull-request review and merge. |

## Verified Git milestones

These are the actual commits on `improve/ten-out-of-ten-masterplan`, in order:

| Commit | Purpose | What changed |
| --- | --- | --- |
| `12ace27` | `refactor: extract world entities and quest progression` | Moved reusable `Thing` and `QuestManager` concepts into `src/`; prevented duplicate quest rewards through a focused system. |
| `7af70e3` | `test: cover quests and complete game flow` | Added headless tests for one-time rewards, victory threshold, loading transition, and the complete fresh playthrough. |
| `f4ccbf0` | `docs: add architecture roadmap and reassessment checklist` | Added evidence-based architecture, roadmap, and QA documentation. |
| `18bda3a` | `feat: humanize neighbourhood dialogue and menu tone` | Improved resident dialogue, emotional pacing, friendly humour, and rotating menu quotes. |

## Verification record

The following checks were run successfully on the development branch:

```text
python -m compileall -q game.py src tests
python -m pytest -q

5 passed
```

The end-to-end test verifies this playable path:

```text
watering can → Deepak → Library storybook → Madhu → Grocery basket → Dhinesh → 30 Trust → Victory
```

## Review and release procedure

1. Open a pull request from `improve/ten-out-of-ten-masterplan` into `main`.
2. Review the checklist in [`evaluation-checklist.md`](evaluation-checklist.md).
3. Confirm tests pass in a clean environment.
4. Merge after approval.
5. Create the `v1.0.0` release tag only after the reviewed branch has merged.

This approach keeps the project presentation professional while preserving an honest, auditable development record.
