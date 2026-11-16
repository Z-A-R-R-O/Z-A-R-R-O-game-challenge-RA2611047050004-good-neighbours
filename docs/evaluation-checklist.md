# Reassessment Checklist

Use this checklist as an evidence record. Keep an item unchecked until the corresponding test or manual check has actually been performed for the current revision.

## Gameplay and completeness

- [x] Game entry point is `game.py`.
- [x] Menu, loading (skippable via Space/Enter/Esc), help, pause, settings, credits, victory, and game-over states are implemented.
- [x] Three quests award Community Trust only once in the quest system.
- [x] Automated full-playthrough test is present.
- [ ] Fresh manual playthrough completed on the current revision.
- [ ] Manual checks completed for interiors, dialogue, collisions, pause/restart, audio, sunset, and victory.

## Architecture and automated testing

- [x] Reusable configuration, world entities, quest logic, and audio systems are split into `src/` (`src/core/config.py`, `src/entities/world.py`, `src/systems/quests.py`, `src/systems/audio.py`).
- [x] Fifteen test functions are present across `tests/test_quests.py`, `tests/test_game_flow.py`, `tests/test_engine.py`, and `tests/test_audio.py`.
- [x] GitHub Actions workflow is configured for Python 3.11 and 3.12.
- [ ] `python -m compileall -q game.py src tests` rerun successfully on the current revision.
- [ ] `python -m pytest -q` rerun successfully on the current revision (15/15).
- [ ] Latest GitHub Actions matrix run verified green on both Python versions.

## Delivery and documentation

- [x] README includes installation, controls, story, screenshots, credits, architecture, and project structure.
- [x] Runtime and development dependencies are separated.
- [x] Development history maps the ten project phases to commit evidence.
- [x] MIT License and author attribution are present.
- [ ] All screenshots and referenced assets checked against the current checkout.
- [ ] Final release notes and tag reviewed after current-revision verification.

## Evidence to attach for final assessment

- [ ] Terminal output showing successful compilation.
- [ ] Terminal output showing all 15 tests passing.
- [ ] GitHub Actions links for Python 3.11 and Python 3.12.
- [ ] Fresh gameplay screenshots or a short screen recording.
