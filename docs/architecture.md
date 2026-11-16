# Architecture

GOOD NEIGHBOURS keeps `game.py` as the required executable entry point while moving independent gameplay concepts into `src/`.

## Runtime flow

```text
game.py (Game)
  ├── src/entities/world.py (Thing)
  ├── src/systems/quests.py (QuestManager)
  ├── Pygame event loop
  ├── state rendering and UI
  └── assets/ (art and optional music)
```

`Game` owns Pygame setup, state transitions, world drawing, input, and asset loading. `QuestManager` owns quest completion, one-time trust rewards, and victory readiness. `Thing` is a small data object shared by NPCs, pickups, entrances, and interior discoveries.

## States

| State | Purpose |
| --- | --- |
| `LOADING` | Timed branded introduction |
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
- `tests/test_game_flow.py` uses headless SDL/Pygame to verify the loading-to-menu transition, skip-loading input, and the full end-to-end victory path.
