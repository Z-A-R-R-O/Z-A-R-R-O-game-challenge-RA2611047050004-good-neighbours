# 10/10 Development Roadmap

This roadmap separates implemented work from final verification. A configured test or workflow is not marked as a successful run until current evidence is available.

| Milestone | Status | Evidence |
| --- | --- | --- |
| Preserve playable baseline | Complete | Existing map, quests, interiors, music, and victory flow retained |
| Establish project lifecycle | Complete | Ten chronological phases with commit references in [development history](development-history.md) |
| Separate reusable systems | Complete | `src/core/config.py`, `src/entities/world.py`, `src/systems/quests.py`, `src/systems/audio.py` |
| Add automated tests | Implemented | 15 test functions across four files in `tests/` |
| Configure automated CI | Implemented | `.github/workflows/ci.yml` targets Python 3.11 and 3.12 |
| Verify current automated suite | Pending | Re-run compileall and pytest on the current revision; retain output |
| Verify current CI matrix | Pending | Confirm the latest GitHub Actions run succeeds on both Python versions |
| Validate full manual playthrough | Pending | Fresh launch and manual checklist for gameplay, UI, audio, and victory |
| Documentation and attribution | Complete | README, architecture, roadmap, development history, evaluation checklist, MIT License |
| Final submission sign-off | Pending | Complete all verification items and attach evidence |

## Final verification commands

```bash
python -m pip install -r requirements-dev.txt
python -m compileall -q game.py src tests
python -m pytest -q
python game.py
```

## Post-submission improvements (optional)

- Split rendering and state handling out of `game.py` incrementally without destabilising the assessed build.
- Add original sound effects and an opt-in save file.
- Add input remapping if scope allows.

Do not delay the assessed submission for optional enhancements. Prioritise reproducible verification and clear evidence.
