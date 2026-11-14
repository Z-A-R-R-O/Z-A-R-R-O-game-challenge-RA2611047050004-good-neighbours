# GOOD NEIGHBOURS

## A Little Town. A Lot of Kindness.

### PROJECT ZARRO --- Game Design & Development Masterfile

> A cozy pixel-art community adventure where the player helps
> neighbours, discovers small stories, and gradually brings an entire
> neighbourhood together.

------------------------------------------------------------------------

## 1. Project Vision

**GOOD NEIGHBOURS** is a peaceful, non-aggressive, top-down pixel-art
adventure about the positive impact of small acts of kindness.

The player explores Maple Street, meets residents, completes helpful
requests, and rebuilds a sense of community. The experience should feel
warm, charming, rewarding, and genuinely enjoyable.

### Core design principles

-   Helpfulness over aggression.
-   Discovery over combat.
-   Meaningful choices over repetitive grinding.
-   Encouraging feedback over harsh punishment.
-   A small, complete experience over an unfinished ambitious game.
-   Every action should make the neighbourhood a little better.

### Creative identity

The game should communicate that ordinary people can make a meaningful
difference through small, thoughtful actions.

------------------------------------------------------------------------

## 2. Official Challenge Compliance

The project must satisfy the department's Python Game Development
Challenge requirements.

### Mandatory requirements

-   A playable game written in Python.
-   Runs from the command line using `python game.py`.
-   Interactive player input and visible game responses.
-   Clear victory and game-over conditions.
-   Score, lives, or level tracking.
-   A help or instructions screen.
-   Graceful handling of invalid input.
-   Organised, commented source code.
-   Meaningful variable and function names.
-   A public GitHub repository on the student's own profile.
-   A completed `README.md`.
-   A `requirements.txt` listing every third-party library used.
-   At least two genuine gameplay screenshots in a `screenshots/`
    folder.
-   No virtual environments, `__pycache__`, or unrelated files in the
    repository.

The work must be individually developed and original. AI assistance may
be used for explanation, doubt-clearing, and debugging, but the student
must author and understand the submitted implementation and be able to
explain every line during evaluation.

------------------------------------------------------------------------

## 3. Game Story

Welcome to **Maple Street**, a small neighbourhood where people have
gradually become disconnected from one another.

The community noticeboard contains several unfinished requests.
Residents need help with ordinary tasks, from returning a lost object to
delivering a book or preparing a neighbourhood gathering.

The player decides to spend an afternoon helping the community
reconnect.

There are no enemies, weapons, combat systems, or destructive
objectives. The challenge comes from exploring, choosing tasks, managing
time, and completing requests.

------------------------------------------------------------------------

## 4. Core Gameplay Loop

1.  Read the community noticeboard.
2.  Explore Maple Street.
3.  Find residents and useful objects.
4.  Interact with residents.
5.  Complete helpful missions.
6.  Earn Community Trust.
7.  Unlock follow-up interactions.
8.  Reach the community goal before the afternoon ends.

### Core player experience

The player should always understand:

-   Where they are.
-   What they can interact with.
-   What each resident needs.
-   Which requests are completed.
-   How much Community Trust they have earned.
-   What they need to do to win.

------------------------------------------------------------------------

## 5. World Design --- Maple Street

Use one compact, top-down map. Avoid building a large open world or
complicated pathfinding system.

### Main locations

1.  **Starting point:** The player's home or neighbourhood entrance.
2.  **Community noticeboard:** Displays available requests and
    objectives.
3.  **Grocery shop:** A place for delivery-related tasks.
4.  **Library:** A place for book-related tasks.
5.  **Community garden and town square:** The main social area and final
    gathering location.

### Environment elements

-   Houses and buildings.
-   Walkable paths.
-   Trees, flowers, benches, and fences.
-   Noticeboard.
-   Shop and library entrances.
-   Community garden.
-   Decorative objects that make the town feel lived in.

### Map implementation

Use a simple tile-based map or a grid of rectangles. Implement solid
objects as collision obstacles. The map should be small enough to
understand quickly and large enough to allow meaningful exploration.

------------------------------------------------------------------------

## 6. Characters and Residents

Create a small cast of memorable residents. Character artwork may be
made from simple pixel-style shapes if external sprites are unavailable.

### Mrs. Eleanor --- The Gardener

-   Needs help finding her missing watering can.
-   Can provide flowers for the community gathering after her request is
    completed.
-   Represents care for shared spaces.

### Leo --- The Little Reader

-   Needs a book delivered from the library.
-   Provides a friendly interaction and a simple delivery mission.
-   Represents curiosity and learning.

### Noah --- The Shopkeeper

-   Needs groceries delivered to a neighbour.
-   Introduces item collection and delivery mechanics.
-   Represents everyday mutual support.

### Maya --- The Community Organiser

-   Needs help preparing the neighbourhood gathering.
-   Can unlock the final community objective.
-   Represents cooperation and connection.

Keep dialogue short, friendly, and easy to understand. Avoid building a
complex dialogue engine for the first version.

------------------------------------------------------------------------

## 7. Mission Design

The initial game should contain three essential missions and one
optional bonus mission.

  Mission                Activity                                    Reward
  ---------------------- --------------------------------------- ----------
  Lost & Found           Find and return the watering can          10 Trust
  A Book for Leo         Collect and deliver a book                10 Trust
  Neighbourly Delivery   Deliver groceries to a neighbour          10 Trust
  The Gathering          Collect items for the community event     10 Trust

The rewards above are proposed game-design values.

### Mission states

Each mission should have a clear state:

-   `locked`
-   `available`
-   `in_progress`
-   `completed`

A completed mission must not award points again.

### Mission interaction flow

1.  Player approaches a resident or mission object.
2.  Player presses the interaction key.
3.  The game checks whether the interaction is valid.
4.  A short dialogue or instruction appears.
5.  The player performs the required action.
6.  The mission manager verifies completion.
7.  The mission is marked completed.
8.  Community Trust is awarded once.
9.  The HUD updates.

### Kindness Chain --- Signature Mechanic

Completing one mission may unlock another.

Example:

-   Help Mrs. Eleanor find her watering can.
-   She offers flowers for the community gathering.
-   Maya uses the flowers to decorate the town square.
-   The town's appearance changes as community progress increases.

For the initial version, implement this using simple mission
dependencies rather than a complicated branching dialogue system.

------------------------------------------------------------------------

## 8. Rules, Scoring, and Progression

### Community Trust

-   Starting Trust: `0`
-   Reward per essential mission: `10`
-   Essential missions: `3`
-   Victory threshold: `30`
-   Optional bonus mission: `10`

### Victory condition

The player wins when Community Trust reaches at least `30`.

### Game-over condition

The afternoon timer expires while Community Trust is below `30`.

### Player-friendly design

-   No combat.
-   No lives system is required.
-   No harsh punishment for mistakes.
-   Restarting begins a fresh playthrough.
-   Completed missions cannot be repeated for extra points.
-   Feedback should be encouraging, even on the game-over screen.

### Suggested play duration

A short playthrough of approximately four to five minutes is
appropriate. The timer should create a light planning challenge, not
unnecessary pressure.

------------------------------------------------------------------------

## 9. Controls

  Input                 Action
  --------------------- ------------------------
  `W` / `Arrow Up`      Move up
  `S` / `Arrow Down`    Move down
  `A` / `Arrow Left`    Move left
  `D` / `Arrow Right`   Move right
  `E`                   Interact
  `H`                   Open help
  `ESC`                 Pause or return
  `R`                   Restart when permitted
  `Q`                   Quit

The help screen must display the actual controls implemented in the
game. Do not document controls that do not work.

------------------------------------------------------------------------

## 10. Visual Direction and Art Style

### Art direction

-   Cozy top-down pixel-art style.
-   Warm, earthy colour palette.
-   Simple, readable character sprites.
-   Compact tile-based environment.
-   Clear interaction indicators.
-   Friendly dialogue boxes.
-   A clean, readable HUD.
-   Subtle visual feedback for completed missions.
-   A visible improvement in the town as progress increases.

### Suggested palette

  Purpose           Colour       Hex
  ----------------- ------------ -----------
  Warm cream        Cream        `#E6D9B8`
  Forest            Green        `#355E4A`
  Terracotta        Orange       `#D98C63`
  Muted sky         Blue         `#7598A5`
  Dark text         Charcoal     `#26332D`
  Soft background   Pale beige   `#F1E9D7`

### Pixel-art specifications

-   Logical tile size: `32 × 32` pixels.
-   Top-down camera.
-   Consistent sprite proportions.
-   Nearest-neighbour scaling if scaling pixel art.
-   Avoid mixing unrelated sprite styles.
-   Prefer original simple shapes if suitable assets are unavailable.

### Asset policy

Use original artwork or assets whose licences permit the intended use.
Credit externally sourced assets in the README. Do not spend excessive
time searching for assets; a coherent game made from simple shapes is
preferable to an unfinished game with elaborate graphics.

------------------------------------------------------------------------

## 11. Interface and Screens

The game should contain the following screens.

### Main Menu

-   Game title.
-   Short subtitle.
-   Start Game.
-   Instructions.
-   Quit.

### Help Screen

-   Objective.
-   Controls.
-   How to interact.
-   How missions work.
-   How Community Trust is earned.
-   Victory and game-over conditions.

### Gameplay HUD

Display:

-   Community Trust.
-   Remaining time.
-   Active mission or objective.
-   Completed mission count.
-   Interaction prompt when near an interactable object.

### Dialogue Screen

Display:

-   Resident name.
-   Short dialogue.
-   Clear interaction or continue instruction.

### Pause Screen

-   Resume.
-   Restart.
-   Quit.

### Victory Screen

-   Congratulatory message.
-   Final Community Trust.
-   Completed missions.
-   Restart.
-   Quit.

### Game-over Screen

-   Friendly message.
-   Progress achieved.
-   Restart.
-   Quit.

------------------------------------------------------------------------

## 12. Technical Stack

### Recommended technology

  Component              Technology
  ---------------------- ------------------------------
  Programming language   Python
  Graphics and input     Pygame
  Game logic             Python functions and classes
  Data structures        Lists and dictionaries
  Optional save data     JSON
  Version control        Git
  Repository hosting     GitHub

Use only dependencies that are genuinely needed.

### Installation

``` bash
python -m pip install pygame
```

### Requirements file

``` text
pygame
```

### Execution

``` bash
python game.py
```

------------------------------------------------------------------------

## 13. Project Architecture

Suggested repository structure:

``` text
game-challenge-ROLLNO-good-neighbours/
│
├── game.py
│
├── modules/
│   ├── settings.py
│   ├── player.py
│   ├── world.py
│   ├── missions.py
│   └── interface.py
│
├── assets/
│   └── (optional original or credited assets)
│
├── screenshots/
│   ├── gameplay.png
│   └── victory.png
│
├── README.md
├── requirements.txt
└── .gitignore
```

### Architecture principle

Start with a working, self-contained `game.py`. Split code into modules
only when separation makes the implementation easier to understand and
maintain.

The root-level `game.py` must remain the executable entry point.

### Main systems

1.  Game state manager.
2.  Main menu.
3.  Player movement.
4.  World rendering.
5.  Collision detection.
6.  Resident and object interaction.
7.  Mission manager.
8.  Community Trust and progression.
9.  HUD and dialogue.
10. Victory and game-over handling.

### Game state model

Suggested states:

-   `MENU`
-   `HELP`
-   `PLAYING`
-   `DIALOGUE`
-   `PAUSED`
-   `VICTORY`
-   `GAME_OVER`

Use a clear state-management approach. Avoid deeply nested conditions in
the main loop.

------------------------------------------------------------------------

## 14. Python Concepts to Demonstrate

The implementation should naturally demonstrate the Python fundamentals
assessed by the department.

  Python concept             Use in GOOD NEIGHBOURS
  -------------------------- ---------------------------------------------
  Variables and data types   Player position, time, score, state
  Conditional statements     Mission checks, collisions, victory
  Loops                      Main game loop and rendering
  Functions                  Movement, drawing, interaction, scoring
  Lists                      Residents, objects, and mission collections
  Dictionaries               Mission definitions and resident data
  Classes and objects        Player, NPC, and game systems
  File handling              Optional saving and loading
  Exception handling         Safe file access and error handling

Do not add concepts artificially. Each concept should have a meaningful
purpose.

------------------------------------------------------------------------

## 15. Engineering Standards

### Code quality

-   Use meaningful names.
-   Keep functions focused.
-   Avoid unnecessarily long functions.
-   Use constants for configuration.
-   Avoid duplicated logic.
-   Use classes where they improve organisation.
-   Comment important decisions and non-obvious logic.
-   Handle invalid states safely.
-   Keep dependencies minimal.

### Pygame engineering

-   Initialise and shut down Pygame correctly.
-   Process events every frame.
-   Maintain a controlled frame rate.
-   Use delta time for movement if appropriate.
-   Separate update logic from rendering.
-   Use collision rectangles or tile-based collision.
-   Avoid blocking delays in the main game loop.
-   Keep keyboard input responsive.
-   Ensure the window can close normally.

### Reliability

Never claim that a feature works unless it has actually been run and
tested.

Do not hide errors with broad exception handlers. Handle expected
failures explicitly and report useful messages when something unexpected
happens.

------------------------------------------------------------------------

## 16. Minimum Viable Product

The first complete version must contain:

-   [ ] Game launches using `python game.py`.
-   [ ] Main menu.
-   [ ] Instructions screen.
-   [ ] Playable Maple Street map.
-   [ ] Player movement.
-   [ ] Collision detection.
-   [ ] At least three interactive residents.
-   [ ] At least three complete missions.
-   [ ] Mission completion tracking.
-   [ ] Community Trust scoring.
-   [ ] Timer.
-   [ ] Victory condition.
-   [ ] Game-over condition.
-   [ ] Restart.
-   [ ] Quit.
-   [ ] Graceful handling of unexpected interactions.

The MVP must be complete before optional polish is added.

------------------------------------------------------------------------

## 17. Optional Enhancements

Only implement these after the MVP is stable.

-   Walking animations.
-   Ambient music.
-   Interaction sound effects.
-   Animated flowers.
-   More resident stories.
-   Fourth chained mission.
-   Decorative town changes as Trust increases.
-   Save/load progression.
-   Weather or sunset effects.
-   Additional neighbourhood locations.

Do not sacrifice core functionality for optional features.

------------------------------------------------------------------------

## 18. Quality Assurance and Testing

Test the following cases.

  Test                          Expected result
  ----------------------------- ----------------------------------
  Launch `python game.py`       Game opens
  Navigate menu                 Correct screen opens
  Open help                     Controls and rules appear
  Move player                   Character responds
  Move into obstacle            Player is blocked
  Interact near resident        Correct interaction appears
  Interact far from resident    No unintended interaction
  Complete a mission            Mission is marked completed
  Complete same mission again   No duplicate reward
  Earn 30 Trust                 Victory screen appears
  Timer expires below 30        Game-over screen appears
  Restart                       New game begins with reset state
  Quit                          Game closes cleanly
  Invalid interaction           Game does not crash
  Missing optional asset        Useful fallback or error message

### Final quality checks

-   No runtime exceptions during normal play.
-   No broken game states.
-   No duplicate scoring.
-   No unresponsive controls.
-   No impossible mission dependencies.
-   No unfair or confusing objectives.
-   No missing required documentation.
-   No uncredited external assets.

------------------------------------------------------------------------

## 19. GitHub Submission

### Repository naming

``` text
game-challenge-ROLLNO-good-neighbours
```

Replace `ROLLNO` with the actual roll number.

### README structure

The README must include:

1.  Game title.
2.  Student name.
3.  Roll number.
4.  Year and section.
5.  Event name.
6.  About the game.
7.  Features.
8.  Controls.
9.  Installation instructions.
10. How to run.
11. Python concepts used.
12. Screenshots.
13. Credits and asset references.

### Suggested `.gitignore`

``` gitignore
__pycache__/
*.py[cod]
.venv/
venv/
.env
.DS_Store
Thumbs.db
```

### Git workflow

Use meaningful commits as development progresses.

Example commit messages:

``` text
Initial project setup
Add player movement and world
Implement resident interactions
Add mission and trust systems
Add victory and game-over states
Complete UI and documentation
```

### Final verification

-   Repository visibility is Public.
-   Repository name follows the required format.
-   `game.py` is at the repository root.
-   The game runs without errors.
-   README is complete.
-   requirements.txt is present.
-   At least two gameplay screenshots are present.
-   No virtual environment or unrelated files are uploaded.
-   Repository opens without logging in.
-   The correct repository URL is submitted through the faculty-provided
    form.

Do not include access tokens, passwords, or other secrets in the
repository.

------------------------------------------------------------------------

## 20. Demonstration and Viva Preparation

Prepare a concise demonstration showing:

1.  The game title and objective.
2.  The controls.
3.  Player movement around Maple Street.
4.  Interaction with a resident.
5.  Mission completion.
6.  Community Trust reward.
7.  Progression toward victory.
8.  The victory or game-over screen.
9.  The GitHub repository.

Be ready to explain:

-   Why Pygame was selected.
-   How the main game loop works.
-   How player movement is implemented.
-   How collision detection works.
-   How NPC interaction is checked.
-   How missions are represented.
-   How Community Trust is calculated.
-   How the victory condition is evaluated.
-   How invalid interactions are handled.
-   How the code is organised.

The student must be able to explain the actual submitted implementation,
including its limitations.

------------------------------------------------------------------------

## 21. Development Partner Instructions

Act as a senior Python engineer, game designer, technical mentor, and
strict code reviewer.

Follow these rules:

1.  Preserve the positive, non-aggressive identity of the game.
2.  Prioritise a complete playable product.
3.  Respect all official challenge requirements.
4.  Keep the implementation achievable and understandable.
5.  Do not introduce unnecessary features or dependencies.
6.  Do not dump an unexplained codebase.
7.  Guide the student through writing and understanding the
    implementation.
8.  Explain important functions, classes, variables, and execution flow.
9.  Help debug actual errors.
10. Never claim untested functionality works.
11. Keep the root `game.py` executable.
12. Recommend sensible trade-offs when decisions arise.
13. Maintain a working build while improving presentation.
14. Keep documentation consistent with the actual implementation.
15. Ensure the student can independently explain the submitted work.

### Recommended implementation order

1.  Project setup and game window.
2.  Main loop and game states.
3.  World map and player movement.
4.  Collision detection.
5.  Residents and interaction.
6.  Mission system.
7.  Community Trust and scoring.
8.  Timer and completion conditions.
9.  Main menu and help screen.
10. Dialogue, HUD, victory, and game-over screens.
11. Testing and debugging.
12. Screenshots, README, requirements, and GitHub verification.

------------------------------------------------------------------------

## 22. Definition of Done

GOOD NEIGHBOURS is complete when:

-   It launches reliably.
-   It is genuinely playable.
-   Its central gameplay loop is enjoyable.
-   Residents and missions work correctly.
-   The player can win and lose.
-   The help screen explains the actual controls.
-   Invalid interactions do not crash the game.
-   The code is organised and explainable.
-   The game has a consistent pixel-art identity.
-   The repository satisfies every submission requirement.
-   The student can demonstrate and explain the implementation.

------------------------------------------------------------------------

# PROJECT ZARRO

## GOOD NEIGHBOURS --- A Little Town. A Lot of Kindness.

**Final objective:** Create an original, technically reliable, charming,
positive, and memorable Python game that demonstrates strong
fundamentals through thoughtful gameplay.

We are not building the biggest game.

We are building the best complete experience we can deliver.
