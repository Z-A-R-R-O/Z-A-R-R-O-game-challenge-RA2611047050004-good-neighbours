# Architecture

GOOD NEIGHBOURS keeps `game.py` as the required executable entry point while moving independent gameplay and configuration concepts into structured `src/` modules.

## Runtime flow

```text
game.py (Game)
  ├── src/core/config.py (display dimensions, world bounds, timing, color palette)
  ├── src/entities/world.py (Thing)
  ├── src/systems/audio.py (AudioManager - background loop, volume clamping, mute)
  ├── src/systems/quests.py (QuestManager - trust, mission tracking, victory flag)
  ├── Pygame event loop & state rendering
  └── assets/ (sprites, backgrounds, and soundtrack)
```

`Game` owns Pygame setup, state transitions, world drawing, input, and asset loading. `QuestManager` owns quest completion, one-time trust rewards, and victory readiness. `Thing` is a small data object shared by NPCs, pickups, entrances, and interior discoveries. `AudioManager` encapsulates sound playback, defensive device handling, and volume controls.

## States

| State | Purpose |
| --- | --- |
| `LOADING` | Timed branded introduction (skippable via Space/Enter/Esc) |
| `MENU` | Start, help, credits, quit |
| `PLAYING` | Maple Street exploration |
| `INTERIOR` | Building exploration |
| `HELP` / `HELP_PLAY` | Contextual controls |
| `PAUSED` / `SETTINGS` | Frozen game and audio controls |
| `CREDITS` | Project attribution |
| `VICTORY` / `GAME_OVER` | End states and replay |

## Test strategy

- `tests/test_quests.py` verifies mission progression, trust rewards, and duplicate prevention independently.
- `tests/test_engine.py` verifies collision blocking, world boundary clamping, afternoon countdown game-over trigger, audio clamping/mute, and lifecycle reset.
- `tests/test_audio.py` tests `AudioManager` in isolation for volume clamping, muting, and defensive missing-asset handling.
- `tests/test_game_flow.py` uses headless SDL/Pygame to verify the loading-to-menu transition, skip-loading input, and the full end-to-end victory path.
