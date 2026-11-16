"""GOOD NEIGHBOURS — a small, friendly Pygame adventure.

Run with: python game.py
"""
from __future__ import annotations

import sys
import math
from pathlib import Path
import pygame
from src.entities.world import Thing
from src.systems.quests import QuestManager

WIDTH, HEIGHT = 1152, 720
FPS = 60
WORLD = pygame.Rect(24, 92, WIDTH - 48, HEIGHT - 116)
PLAYER_SPEED = 220
AFTERNOON_SECONDS = 480
LOADING_SECONDS = 8.0

# Warm, readable palette. All artwork is drawn in code, so no external assets are needed.
CREAM = (241, 233, 215)
PAPER = (230, 217, 184)
GREEN = (53, 94, 74)
LIGHT_GREEN = (111, 151, 103)
SKY = (117, 152, 165)
TERRACOTTA = (217, 140, 99)
CHARCOAL = (38, 51, 45)
GOLD = (235, 190, 77)
WHITE = (255, 250, 240)
RED = (185, 83, 74)


class Game:
    def __init__(self) -> None:
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            # Audio is optional: the game remains playable on devices without an audio driver.
            pass
        pygame.display.set_caption("GOOD NEIGHBOURS — A Little Town. A Lot of Kindness.")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 25)
        self.small = pygame.font.Font(None, 20)
        self.title = pygame.font.Font(None, 52)
        self.logo = pygame.font.Font(None, 76)
        self.music_volume = 0.28
        self.music_muted = False
        self.menu_quotes = [
            "\"Small kindnesses make very loud happiness.\"",
            "\"A good neighbour knows where the spare biscuits are.\"",
            "\"The watering can is not lost. It is on a tiny adventure.\"",
            "\"Every street is better with one more hello.\"",
            "\"Maple Street runs on tea, trust, and occasionally borrowed ladders.\"",
        ]
        self.load_assets()
        self.start_ambient_music()
        self.state = "LOADING"
        self.loading_elapsed = 0.0
        self.reset()

    def load_assets(self) -> None:
        """Load generated art once, then crop it into usable top-down sprites."""
        asset_dir = Path(__file__).with_name("assets")
        self.loading_art = pygame.image.load(asset_dir / "maple_street_loading.png").convert()
        self.loading_art = pygame.transform.smoothscale(self.loading_art, (WIDTH, HEIGHT))
        self.victory_art = pygame.image.load(asset_dir / "victory_gathering.png").convert()
        self.victory_art = pygame.transform.smoothscale(self.victory_art, (WIDTH, HEIGHT))
        self.ground_art = pygame.image.load(asset_dir / "maple_street_ground.png").convert()
        self.ground_art = pygame.transform.smoothscale(self.ground_art, WORLD.size)
        self.library_interior = pygame.image.load(asset_dir / "library_interior.png").convert()
        self.library_interior = pygame.transform.smoothscale(self.library_interior, (WIDTH, HEIGHT))
        interior_sheet = pygame.image.load(asset_dir / "building_interiors.png").convert()
        sw, sh = interior_sheet.get_size()
        self.building_interiors = [pygame.transform.smoothscale(interior_sheet.subsurface(pygame.Rect(i * sw // 3, 0, sw // 3, sh)), (WIDTH, HEIGHT)) for i in range(3)]
        residents = pygame.image.load(asset_dir / "residents_topdown.png").convert_alpha()
        world = pygame.image.load(asset_dir / "topdown_world_sheet.png").convert_alpha()
        rw, rh = residents.get_size()
        ww, wh = world.get_size()
        # Generated sheets are intentionally divided into broad, transparent cells.
        self.resident_art = [residents.subsurface(pygame.Rect(i * rw // 4, 0, rw // 4, rh)).copy() for i in range(4)]
        self.tree_art = [world.subsurface(pygame.Rect(i * ww // 4, 0, ww // 4, wh * 31 // 100)).copy() for i in range(4)]
        self.building_art = [world.subsurface(pygame.Rect(i * ww // 4, wh * 29 // 100, ww // 4, wh * 35 // 100)).copy() for i in range(4)]
        self.notice_art = world.subsurface(pygame.Rect(ww * 3 // 4, wh * 62 // 100, ww // 4, wh * 25 // 100)).copy()
        self.player_art = pygame.image.load(asset_dir / "player_neighbour.png").convert_alpha()
        self.river_art = pygame.image.load(asset_dir / "river_bridge.png").convert_alpha()
        self.logo_art = pygame.image.load(asset_dir / "good_neighbours_logo.png").convert_alpha()
        item_sheet = pygame.image.load(asset_dir / "collectible_items.png").convert_alpha()
        iw, ih = item_sheet.get_size()
        self.item_art = [item_sheet.subsurface(pygame.Rect(i * iw // 3, 0, iw // 3, ih)).copy() for i in range(3)]
        portraits = pygame.image.load(asset_dir / "resident_portraits.png").convert_alpha()
        pw, ph = portraits.get_size()
        self.portraits = [portraits.subsurface(pygame.Rect(i * pw // 4, 0, pw // 4, ph)).copy() for i in range(4)]

    def start_ambient_music(self) -> None:
        """Play an optional, project-owned ambient loop when one is available."""
        asset_dir = Path(__file__).with_name("assets")
        # Prefer the approved project soundtrack; retain OGG as a lightweight fallback.
        track = asset_dir / "good_neighbours_bg.mp3"
        if not track.exists():
            track = asset_dir / "ambient.ogg"
        if not track.exists() or not pygame.mixer.get_init():
            return
        try:
            pygame.mixer.music.load(track)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
        except pygame.error:
            # An invalid optional audio file must never prevent the game from launching.
            return

    def reset(self) -> None:
        self.player = pygame.Rect(365, 550, 24, 28)
        self.quests = QuestManager()
        self.time_left = float(AFTERNOON_SECONDS)
        self.message = "Maple Street used to share every little thing. Today, a few kind errands can bring that warmth back."
        self.message_timer = 7.0
        self.message_visible = 0.0
        self.dialogue_active = False
        self.speaker = "Maple Street"
        self.game_time = 0.0
        self.inventory: set[str] = set()
        # Solid buildings and fences: moving into one is safely blocked.
        self.walls = [
            pygame.Rect(155, 168, 170, 112), pygame.Rect(735, 168, 170, 112),
            pygame.Rect(155, 460, 165, 110), pygame.Rect(740, 460, 155, 125),
            pygame.Rect(448, 315, 200, 18), pygame.Rect(448, 315, 18, 130),
            pygame.Rect(630, 315, 18, 130),
            # Willow River is solid water; the central gap aligns with the bridge.
            pygame.Rect(976, 110, 108, 220), pygame.Rect(976, 400, 108, 250),
        ]
        self.npcs = [
            Thing("Deepak", pygame.Rect(532, 375, 26, 32), TERRACOTTA, "eleanor"),
            Thing("Madhu", pygame.Rect(328, 292, 26, 32), SKY, "leo"),
            Thing("Dhinesh", pygame.Rect(705, 292, 26, 32), GREEN, "noah"),
            Thing("Nethra", pygame.Rect(670, 510, 26, 32), GOLD, "maya"),
        ]
        self.items = [
            Thing("watering can", pygame.Rect(380, 190, 22, 18), SKY, "can"),
            # Kept beside the Library (not inside its collision rectangle) so it is collectible.
            Thing("library book", pygame.Rect(840, 304, 24, 26), TERRACOTTA, "book"),
            Thing("groceries", pygame.Rect(410, 480, 28, 25), GOLD, "groceries"),
        ]
        self.entries = [
            Thing("Library", pygame.Rect(230, 270, 28, 18), GREEN, "enter_library"),
            Thing("Home", pygame.Rect(230, 568, 28, 18), GREEN, "enter_home"),
            Thing("Grocery", pygame.Rect(810, 270, 28, 18), GREEN, "enter_grocery"),
            Thing("Town Hall", pygame.Rect(810, 585, 28, 18), GREEN, "enter_hall"),
        ]
        self.current_interior = "library"
        self.return_position = (244, 302)
        self.interior_items = [Thing("reading journal", pygame.Rect(392, 585, 26, 22), TERRACOTTA, "journal")]
        self.discovered: set[str] = set()

    def set_message(self, text: str, speaker: str | None = None) -> None:
        """Start a fresh, typewriter-style line of dialogue."""
        self.message, self.message_visible = text, 0.0
        self.dialogue_active = True
        if speaker is not None:
            self.speaker = speaker

    def move_player(self, dx: float, dy: float) -> None:
        # Axis-separated collision lets the player slide naturally along walls.
        self.player.x += round(dx)
        if self.player.left < WORLD.left or self.player.right > WORLD.right or any(self.player.colliderect(w) for w in self.walls):
            self.player.x -= round(dx)
        self.player.y += round(dy)
        if self.player.top < WORLD.top or self.player.bottom > WORLD.bottom or any(self.player.colliderect(w) for w in self.walls):
            self.player.y -= round(dy)

    def nearest(self) -> Thing | None:
        if self.state == "INTERIOR":
            choices = [Thing("Maple Street", pygame.Rect(WIDTH // 2 - 25, HEIGHT - 74, 50, 25), GREEN, "exit_library")]
            choices += [item for item in self.interior_items if item.kind not in self.discovered]
            inside_item = {"library": "book", "grocery": "groceries"}.get(self.current_interior)
            if inside_item:
                choices += [item for item in self.items if item.kind == inside_item and item.kind not in self.inventory]
        else:
            choices = self.npcs + self.entries + [i for i in self.items if i.kind not in self.inventory]
        close = [thing for thing in choices if self.player.centerx - 42 <= thing.rect.centerx <= self.player.centerx + 42
                 and self.player.centery - 42 <= thing.rect.centery <= self.player.centery + 42]
        return close[0] if close else None

    def award(self, mission: str, text: str) -> None:
        if self.quests.complete(mission):
            self.set_message(text + "  +10 Community Trust!")

    def interact(self) -> None:
        thing = self.nearest()
        if thing is None:
            self.set_message("Nothing to help with here just yet. Follow the gold beacon—Maple Street is quietly counting on you.", "Maple Street")
            return
        if thing.kind.startswith("enter_"):
            self.return_position = {
                "enter_library": (244, 302), "enter_home": (244, 586),
                "enter_grocery": (824, 302), "enter_hall": (824, 600),
            }[thing.kind]
            self.state = "INTERIOR"
            self.current_interior = thing.kind.removeprefix("enter_")
            self.player.center = (WIDTH // 2, HEIGHT - 100)
            places = {"library": "Maple Street Library", "home": "Home", "grocery": "Dhinesh's Grocery", "hall": "Town Hall"}
            self.set_message(f"Welcome to {places[self.current_interior]}. Take a look around; every room has a little piece of Maple Street's story.", places[self.current_interior])
            return
        if thing.kind == "exit_library":
            self.state = "PLAYING"
            self.player.center = self.return_position
            self.set_message("You step back into the afternoon light. Somewhere nearby, a neighbour is probably pretending they do not need help.", "Maple Street")
            return
        if thing.kind in ("journal", "map"):
            self.discovered.add(thing.kind)
            text = ("The reading journal records every favour traded on Maple Street. No grand speeches—just names, dates, and little moments that made someone feel less alone."
                    if thing.kind == "journal" else "The old map marks a quiet footpath beside Willow River. Someone has drawn a tiny heart beside the bridge. Very official cartography.")
            self.set_message(text, "Library")
            return
        if thing.kind in ("can", "book", "groceries"):
            self.inventory.add(thing.kind)
            labels = {"can": "watering can", "book": "library book", "groceries": "groceries"}
            self.set_message(f"You picked up the {labels[thing.kind]}. One small errand closer to a much brighter street.", "Maple Street")
            return
        self.speaker = thing.name
        if thing.kind == "eleanor":
            if "can" in self.inventory:
                self.award("can", "Deepak's shoulders soften. 'There you are! The garden was beginning to look at me like I had forgotten its birthday. Thank you, neighbour.'")
            elif self.quests.is_completed("can"):
                self.set_message("The garden is already perking up. 'Funny how one helpful hand can make a whole street feel closer,' Deepak says.")
            else:
                self.set_message("'My watering can wandered off near the old oak,' Deepak says. 'It has always had a dramatic streak. Could you take a look?' ")
        elif thing.kind == "leo":
            if "book" in self.inventory:
                self.award("book", "Madhu hugs the book to their chest. 'Perfect! I will read this aloud at the gathering. Nobody should have to miss the good part.'")
            elif self.quests.is_completed("book"):
                self.set_message("'My favourite stories are the ones neighbours make together,' Madhu says, carefully saving your place with a leaf.")
            else:
                self.set_message("'The library saved a storybook for me,' Madhu says. 'Would you bring it over before the gathering? I promise I will not skip ahead. Much.'")
        elif thing.kind == "noah":
            if "groceries" in self.inventory:
                self.award("groceries", "Dhinesh sets the basket on the counter with a grin. 'A shared table is how a street becomes a neighbourhood—and this one was missing carrots.'")
            elif self.quests.is_completed("groceries"):
                self.set_message("'Maple Street is lucky to have a neighbour who notices the small things,' Dhinesh says. 'The small things are where the good stuff hides.'")
            else:
                self.set_message("'I am preparing snacks for Nethra's gathering,' Dhinesh says. 'The grocery basket is waiting inside. Please rescue it before the cucumbers start acting important.'")
        elif thing.kind == "maya":
            if self.quests.victory_reached:
                self.state = "VICTORY"
            else:
                needed = 30 - self.quests.trust
                self.set_message(f"'We need {needed} more Trust before the lanterns can be lit,' Nethra says. 'Every small kindness counts—especially the ones no one puts on a poster.'")

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type != pygame.KEYDOWN:
            return
        key = event.key
        if self.state == "LOADING":
            if key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                self.state = "MENU"
        elif self.state == "MENU":
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.state = "PLAYING"
            elif key == pygame.K_h:
                self.state = "HELP"
            elif key == pygame.K_c:
                self.state = "CREDITS"
            elif key in (pygame.K_q, pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        elif self.state == "HELP":
            if key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_h):
                self.state = "MENU"
        elif self.state == "CREDITS":
            if key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_c):
                self.state = "MENU"
        elif self.state in ("PLAYING", "INTERIOR"):
            if key == pygame.K_e:
                if self.dialogue_active:
                    if self.message_visible < len(self.message):
                        self.message_visible = float(len(self.message))
                    else:
                        self.dialogue_active = False
                else:
                    self.interact()
            elif key in (pygame.K_ESCAPE, pygame.K_p):
                self.state = "PAUSED"
            elif key == pygame.K_h:
                self.state = "HELP_PLAY"
            elif key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif self.state == "HELP_PLAY":
            if key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_h):
                self.state = "PLAYING"
        elif self.state == "PAUSED":
            if key in (pygame.K_ESCAPE, pygame.K_p, pygame.K_RETURN):
                self.state = "PLAYING"
            elif key == pygame.K_s:
                self.state = "SETTINGS"
            elif key == pygame.K_r:
                self.reset()
                self.state = "PLAYING"
            elif key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif self.state == "SETTINGS":
            if key in (pygame.K_ESCAPE, pygame.K_s, pygame.K_RETURN):
                self.state = "PAUSED"
            elif key == pygame.K_m:
                self.toggle_music()
            elif key in (pygame.K_RIGHT, pygame.K_UP, pygame.K_EQUALS):
                self.change_music_volume(0.05)
            elif key in (pygame.K_LEFT, pygame.K_DOWN, pygame.K_MINUS):
                self.change_music_volume(-0.05)
        elif self.state in ("VICTORY", "GAME_OVER"):
            if key == pygame.K_r:
                self.reset()
                self.state = "PLAYING"
            elif key in (pygame.K_q, pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def update(self, dt: float) -> None:
        if self.state == "LOADING":
            self.loading_elapsed += dt
            if self.loading_elapsed >= LOADING_SECONDS:
                self.state = "MENU"
            return
        if self.state not in ("PLAYING", "INTERIOR"): return
        if self.dialogue_active:
            self.message_visible = min(len(self.message), self.message_visible + dt * 58)
            return
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        if dx or dy:
            length = max(1, (dx * dx + dy * dy) ** 0.5)
            if self.state == "INTERIOR":
                self.player.x = max(40, min(WIDTH - self.player.width - 40, self.player.x + round(dx / length * PLAYER_SPEED * dt)))
                self.player.y = max(135, min(HEIGHT - self.player.height - 70, self.player.y + round(dy / length * PLAYER_SPEED * dt)))
            else:
                self.move_player(dx / length * PLAYER_SPEED * dt, dy / length * PLAYER_SPEED * dt)
        self.time_left -= dt
        self.game_time += dt
        self.message_visible = min(len(self.message), self.message_visible + dt * 58)
        if self.quests.victory_reached:
            self.state = "VICTORY"
        elif self.time_left <= 0:
            self.state = "GAME_OVER"

    def text(self, value: str, pos: tuple[int, int], color=CHARCOAL, font=None, center=False) -> None:
        image = (font or self.font).render(value, True, color)
        rect = image.get_rect(center=pos) if center else image.get_rect(topleft=pos)
        self.screen.blit(image, rect)

    def panel(self, rect: pygame.Rect, color=PAPER) -> None:
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, CHARCOAL, rect, 2, border_radius=10)

    def blit_scaled(self, image: pygame.Surface, rect: pygame.Rect) -> None:
        """Scale assets at draw time; source art stays high-resolution and crisp."""
        self.screen.blit(pygame.transform.smoothscale(image, rect.size), rect)

    def wrapped_lines(self, value: str, max_width: int, font=None) -> list[str]:
        """Wrap dialogue safely instead of allowing it to run off a panel."""
        chosen = font or self.small
        words, lines, current = value.split(), [], ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if current and chosen.size(candidate)[0] > max_width:
                lines.append(current)
                current = word
            else:
                current = candidate
        return lines + ([current] if current else [])

    def objective_target(self) -> Thing | None:
        """Return the next useful thing so the guide never points at a completed task."""
        plan = (("can", "eleanor"), ("book", "leo"), ("groceries", "noah"))
        for item_kind, npc_kind in plan:
            if self.quests.is_completed(item_kind):
                continue
            if item_kind in self.inventory:
                return next(npc for npc in self.npcs if npc.kind == npc_kind)
            required_entry = {"book": "enter_library", "groceries": "enter_grocery"}.get(item_kind)
            if required_entry and self.state != "INTERIOR":
                return next(entry for entry in self.entries if entry.kind == required_entry)
            return next((item for item in self.items if item.kind == item_kind), None)
        return next(npc for npc in self.npcs if npc.kind == "maya")

    def objective_text(self) -> str:
        target = self.objective_target()
        if target is None:
            return "Explore Maple Street"
        if target.kind in ("can", "book", "groceries"):
            return f"Find: {target.name}"
        return f"Visit: {target.name}"

    def draw_item_icon(self, kind: str, box: pygame.Rect, muted: bool = False) -> None:
        index = {"can": 0, "book": 1, "groceries": 2}[kind]
        sprite = self.item_art[index].copy()
        if muted:
            sprite.set_alpha(90)
        self.blit_scaled(sprite, box.inflate(-4, -4))

    def change_music_volume(self, amount: float) -> None:
        self.music_volume = max(0.0, min(1.0, self.music_volume + amount))
        self.music_muted = self.music_volume == 0
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(0 if self.music_muted else self.music_volume)

    def toggle_music(self) -> None:
        self.music_muted = not self.music_muted
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(0 if self.music_muted else self.music_volume)

    def draw_flowerbed(self, rect: pygame.Rect, colors: tuple[tuple[int, int, int], ...]) -> None:
        """Small hand-drawn garden beds fill the town without obscuring routes."""
        pygame.draw.rect(self.screen, (99, 134, 73), rect, border_radius=9)
        pygame.draw.rect(self.screen, (62, 91, 54), rect, 2, border_radius=9)
        for x in range(rect.left + 11, rect.right - 4, 17):
            y = rect.top + 13 + ((x // 17) % 2) * 10
            pygame.draw.circle(self.screen, colors[(x // 17) % len(colors)], (x, y), 5)
            pygame.draw.circle(self.screen, GOLD, (x, y), 2)

    def draw_world(self) -> None:
        self.screen.fill(CREAM)
        # One authored terrain image gives every walkable area a coherent identity.
        self.screen.blit(self.ground_art, WORLD.topleft)
        # Buildings / obstacles
        buildings = [(self.walls[0], "LIBRARY", 2), (self.walls[1], "GROCERY", 3), (self.walls[2], "HOME", 0), (self.walls[3], "TOWN HALL", 1)]
        for rect, label, art_index in buildings:
            self.blit_scaled(self.building_art[art_index], rect.inflate(22, 18))
            place_tag = pygame.Rect(0, 0, self.small.size(label)[0] + 18, 21)
            place_tag.center = (rect.centerx, rect.bottom - 16)
            pygame.draw.rect(self.screen, (25, 43, 35), place_tag, border_radius=6)
            pygame.draw.rect(self.screen, GOLD, place_tag, 1, border_radius=6)
            self.text(label, place_tag.center, WHITE, self.small, center=True)
        # Native top-down decorative sprites turn the rectangle map into Maple Street.
        self.text("WILLOW RIVER", (1067, 675), SKY, self.small, center=True)
        # Garden fence: visible warm wood, not a solid collision-coloured block.
        for wall in self.walls[4:7]:
            pygame.draw.rect(self.screen, (107, 70, 43), wall, border_radius=2)
            pygame.draw.rect(self.screen, (182, 126, 71), wall.inflate(-4, -4), border_radius=2)
            if wall.width > wall.height:
                for x in range(wall.left + 10, wall.right, 26):
                    pygame.draw.rect(self.screen, (82, 54, 35), (x, wall.top - 6, 6, wall.height + 12), border_radius=2)
            else:
                for y in range(wall.top + 10, wall.bottom, 26):
                    pygame.draw.rect(self.screen, (82, 54, 35), (wall.left - 6, y, wall.width + 12, 6), border_radius=2)
        garden_tag = pygame.Rect(469, 334, 158, 22)
        pygame.draw.rect(self.screen, (25, 43, 35), garden_tag, border_radius=6)
        pygame.draw.rect(self.screen, GOLD, garden_tag, 1, border_radius=6)
        self.text("COMMUNITY GARDEN", garden_tag.center, WHITE, self.small, center=True)
        # Noticeboard
        board = pygame.Rect(324, 228, 62, 76)
        self.blit_scaled(self.notice_art, board)
        for index, item in enumerate(self.items):
            if item.kind not in self.inventory and item.kind not in ("book", "groceries"):
                # A gentle hover makes collectables readable before the player reaches them.
                bob = int(math.sin(self.game_time * 3 + index) * 4)
                floating = item.rect.move(0, bob)
                pygame.draw.ellipse(self.screen, (88, 123, 76), floating.inflate(8, -10))
                self.draw_item_icon(item.kind, floating.inflate(8, 8))
        for art_index, npc in enumerate(self.npcs):
            self.blit_scaled(self.resident_art[art_index], npc.rect.inflate(17, 16))
            name_box = pygame.Rect(0, 0, self.small.size(npc.name)[0] + 12, 19)
            name_box.midtop = (npc.rect.centerx, npc.rect.bottom + 3)
            pygame.draw.rect(self.screen, (25, 43, 35), name_box, border_radius=5)
            self.text(npc.name, name_box.center, WHITE, self.small, center=True)
        # The player uses an original illustrated sprite rather than a coloured block.
        pygame.draw.ellipse(self.screen, (74, 105, 70), self.player.inflate(12, -12))
        self.blit_scaled(self.player_art, self.player.inflate(22, 28))
        you_tag = pygame.Rect(0, 0, 38, 18)
        you_tag.midtop = (self.player.centerx, self.player.bottom + 9)
        pygame.draw.rect(self.screen, (25, 43, 35), you_tag, border_radius=5)
        pygame.draw.rect(self.screen, GOLD, you_tag, 1, border_radius=5)
        self.text("YOU", you_tag.center, WHITE, self.small, center=True)
        near = self.nearest()
        target = self.objective_target()
        if target:
            arrow_y = target.rect.top - 22 + int(math.sin(self.game_time * 4) * 4)
            # A pulsing beacon and label make the current objective immediately legible.
            pulse = 16 + int((math.sin(self.game_time * 5) + 1) * 3)
            pygame.draw.circle(self.screen, (255, 235, 132), target.rect.center, pulse, 2)
            pygame.draw.polygon(self.screen, GOLD, [(target.rect.centerx, arrow_y + 12), (target.rect.centerx - 8, arrow_y), (target.rect.centerx + 8, arrow_y)])
            pygame.draw.polygon(self.screen, CHARCOAL, [(target.rect.centerx, arrow_y + 12), (target.rect.centerx - 8, arrow_y), (target.rect.centerx + 8, arrow_y)], 1)
            distance = max(1, int(math.dist(self.player.center, target.rect.center) / 32))
            guide = f"NEXT  •  {self.objective_text()}  •  {distance} tiles"
            label = pygame.Rect(0, 0, min(330, self.font.size(guide)[0] + 28), 27)
            label.midtop = (WIDTH // 2, 82)
            self.panel(label, WHITE)
            self.text(guide, label.center, GREEN, self.small, center=True)
        if near:
            prompt = "Pick up" if near.kind in ("can", "book", "groceries") else "Talk to"
            tag = pygame.Rect(0, 0, 230, 31)
            tag.midbottom = (near.rect.centerx, near.rect.top - 10)
            self.panel(tag, WHITE)
            self.text(f"[E] {prompt} {near.name}", tag.center, CHARCOAL, self.small, center=True)

    def draw_hud(self) -> None:
        pygame.draw.rect(self.screen, CHARCOAL, (0, 0, WIDTH, 76))
        self.text(f"COMMUNITY TRUST  {self.quests.trust}/30", (24, 12), WHITE)
        elapsed = 1 - max(0, self.time_left) / AFTERNOON_SECONDS
        map_minutes = 16 * 60 + int(elapsed * 180)  # 4:00 PM → 7:00 PM over one play session.
        hour24, minute = divmod(map_minutes, 60)
        suffix = "PM" if hour24 >= 12 else "AM"
        hour12 = hour24 % 12 or 12
        clock_center = (WIDTH - 276, 25)
        self.text(f"MAPLE TIME  {hour12}:{minute:02} {suffix}", (WIDTH - 255, 12), WHITE)
        pygame.draw.circle(self.screen, PAPER, clock_center, 12)
        pygame.draw.circle(self.screen, CHARCOAL, clock_center, 12, 2)
        angle = -1.5708 + elapsed * 6.283
        hand = (clock_center[0] + int(math.cos(angle) * 8), clock_center[1] + int(math.sin(angle) * 8))
        pygame.draw.line(self.screen, TERRACOTTA, clock_center, hand, 2)
        pygame.draw.rect(self.screen, (72, 88, 78), (WIDTH - 230, 45, 190, 5), border_radius=3)
        pygame.draw.rect(self.screen, GOLD, (WIDTH - 230, 45, int(190 * max(0, self.time_left) / AFTERNOON_SECONDS), 5), border_radius=3)
        self.text("SUNSET APPROACHES", (WIDTH - 135, 58), PAPER, self.small, center=True)
        completed = self.quests.completed_count
        self.text(f"Kindness missions: {completed}/3", (24, 39), PAPER, self.small)
        self.text(self.objective_text(), (24, 57), GOLD, self.small)
        # Dynamic hotbar: it is absent until the player has earned their first item.
        carried = [kind for kind in ("can", "book", "groceries") if kind in self.inventory]
        if carried:
            total_width = len(carried) * 56
            start_x = WIDTH // 2 - total_width // 2
            self.text("PACK", (start_x - 42, 38), PAPER, self.small, center=True)
        for index, kind in enumerate(carried):
            slot = pygame.Rect(start_x + index * 56, 18, 46, 46)
            pygame.draw.rect(self.screen, (82, 91, 78), slot, border_radius=4)
            pygame.draw.rect(self.screen, GOLD, slot, 2, border_radius=4)
            self.draw_item_icon(kind, slot)
            self.text(str(index + 1), (slot.left + 4, slot.top + 2), WHITE, self.small)
        if self.dialogue_active:
            # Conversations pause the world and use resident portraits as a proper cutscene.
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((14, 25, 18, 58))
            self.screen.blit(shade, (0, 0))
            box = pygame.Rect(76, HEIGHT - 180, 850, 128)
            self.panel(box, WHITE)
            portrait_index = {"Deepak": 0, "Madhu": 1, "Dhinesh": 2, "Nethra": 3}.get(self.speaker)
            if portrait_index is not None:
                self.blit_scaled(self.portraits[portrait_index], pygame.Rect(box.left + 8, box.top - 56, 142, 174))
            else:
                pygame.draw.circle(self.screen, TERRACOTTA, (box.left + 58, box.centery), 34)
                pygame.draw.circle(self.screen, WHITE, (box.left + 48, box.centery - 6), 5)
                pygame.draw.circle(self.screen, WHITE, (box.left + 68, box.centery - 6), 5)
            speaker_box = pygame.Rect(box.left + 144, box.top - 18, max(130, self.font.size(self.speaker)[0] + 30), 30)
            pygame.draw.rect(self.screen, GREEN, speaker_box, border_radius=6)
            self.text(self.speaker, speaker_box.center, WHITE, self.small, center=True)
            shown = self.message[:int(self.message_visible)]
            for line_index, line in enumerate(self.wrapped_lines(shown, 650, self.font)):
                self.text(line, (box.left + 160, box.top + 27 + line_index * 22), CHARCOAL, self.font)
            if int(self.message_visible) < len(self.message):
                self.text("…", (box.right - 30, box.bottom - 26), TERRACOTTA, self.font, center=True)
            else:
                self.text("[E] Continue", (box.right - 70, box.bottom - 24), GREEN, self.small, center=True)

    def draw_interior(self) -> None:
        """Render a small interior scene with readable examine/exit interactions."""
        backgrounds = {"library": self.library_interior, "home": self.building_interiors[0], "grocery": self.building_interiors[1], "hall": self.building_interiors[2]}
        labels = {"library": "MAPLE STREET LIBRARY", "home": "HOME", "grocery": "DHINESH'S GROCERY", "hall": "TOWN HALL"}
        self.screen.blit(backgrounds[self.current_interior], (0, 0))
        title_box = pygame.Rect(WIDTH // 2 - 155, 88, 310, 31)
        pygame.draw.rect(self.screen, (25, 43, 35), title_box, border_radius=8)
        pygame.draw.rect(self.screen, GOLD, title_box, 2, border_radius=8)
        self.text(labels[self.current_interior], title_box.center, WHITE, self.small, center=True)
        for item in self.interior_items:
            if item.kind in self.discovered or self.current_interior != "library":
                continue
            glow = item.rect.inflate(18, 18)
            pygame.draw.ellipse(self.screen, (255, 220, 100), glow, 2)
            self.draw_item_icon("book" if item.kind == "journal" else "groceries", item.rect.inflate(6, 6))
        active_item = {"library": "book", "grocery": "groceries"}.get(self.current_interior)
        if active_item and active_item not in self.inventory:
            pickup = next(item for item in self.items if item.kind == active_item)
            pygame.draw.ellipse(self.screen, (255, 220, 100), pickup.rect.inflate(20, 20), 2)
            self.draw_item_icon(active_item, pickup.rect.inflate(7, 7))
        pygame.draw.ellipse(self.screen, (64, 60, 47), self.player.inflate(15, -12))
        # Larger indoor player sprite matches the room scale and makes navigation easier to read.
        self.blit_scaled(self.player_art, self.player.inflate(42, 52))
        exit_rect = pygame.Rect(WIDTH // 2 - 62, HEIGHT - 74, 124, 25)
        pygame.draw.rect(self.screen, (25, 43, 35), exit_rect, border_radius=6)
        self.text("DOOR TO MAPLE ST.", exit_rect.center, WHITE, self.small, center=True)
        near = self.nearest()
        if near:
            action = "Leave" if near.kind == "exit_library" else "Examine"
            prompt = pygame.Rect(0, 0, 220, 30)
            prompt.midbottom = (near.rect.centerx, max(130, near.rect.top - 8))
            self.panel(prompt, WHITE)
            self.text(f"[E] {action}: {near.name}", prompt.center, CHARCOAL, self.small, center=True)

    def overlay(self, heading: str, lines: list[str], footer: str) -> None:
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((20, 30, 25, 185))
        self.screen.blit(shade, (0, 0))
        box = pygame.Rect(145, 100, 670, 430)
        self.panel(box, CREAM)
        self.text(heading, (WIDTH // 2, 155), GREEN, self.title, center=True)
        for index, line in enumerate(lines):
            self.text(line, (WIDTH // 2, 220 + index * 32), CHARCOAL, self.font, center=True)
        self.text(footer, (WIDTH // 2, 485), TERRACOTTA, self.font, center=True)

    def draw_settings(self) -> None:
        """A focused settings card that remains readable over the living map."""
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((16, 28, 20, 195))
        self.screen.blit(shade, (0, 0))
        box = pygame.Rect(280, 148, 590, 415)
        self.panel(box, CREAM)
        self.text("SETTINGS", (box.centerx, box.top + 55), GREEN, self.title, center=True)
        self.text("SOUND & COMFORT", (box.centerx, box.top + 91), TERRACOTTA, self.small, center=True)
        icon_box = pygame.Rect(box.left + 56, box.top + 142, 58, 58)
        pygame.draw.rect(self.screen, GREEN, icon_box, border_radius=10)
        self.text("ON" if not self.music_muted else "OFF", icon_box.center, WHITE, self.small, center=True)
        state = "ON" if not self.music_muted else "MUTED"
        self.text(f"Ambient music  •  {state}", (box.left + 140, box.top + 151), CHARCOAL, self.font)
        percent = int(self.music_volume * 100) if not self.music_muted else 0
        self.text(f"Volume {percent}%", (box.left + 140, box.top + 181), GREEN, self.small)
        bar = pygame.Rect(box.left + 140, box.top + 215, 355, 14)
        pygame.draw.rect(self.screen, (100, 111, 95), bar, border_radius=7)
        pygame.draw.rect(self.screen, GOLD, (bar.left, bar.top, int(bar.width * percent / 100), bar.height), border_radius=7)
        knob_x = bar.left + int(bar.width * percent / 100)
        pygame.draw.circle(self.screen, WHITE, (knob_x, bar.centery), 10)
        self.text("M  Mute / unmute", (box.centerx, box.top + 278), CHARCOAL, self.font, center=True)
        self.text("LEFT / RIGHT   Adjust volume", (box.centerx, box.top + 313), CHARCOAL, self.font, center=True)
        self.text("ESC / S / ENTER   Back to pause", (box.centerx, box.bottom - 42), TERRACOTTA, self.font, center=True)

    def draw_victory(self) -> None:
        """Celebratory finale artwork with a quiet readable conclusion panel."""
        self.screen.blit(self.victory_art, (0, 0))
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((15, 38, 30, 110))
        self.screen.blit(shade, (0, 0))
        panel = pygame.Rect(202, 88, 748, 244)
        pygame.draw.rect(self.screen, (21, 54, 42), panel, border_radius=16)
        pygame.draw.rect(self.screen, GOLD, panel, 3, border_radius=16)
        self.text("THE STREET COMES TOGETHER!", (panel.centerx, panel.top + 52), WHITE, self.title, center=True)
        self.text(f"{self.quests.trust} COMMUNITY TRUST", (panel.centerx, panel.top + 102), GOLD, self.font, center=True)
        self.text("Your kindness brought Maple Street to life.", (panel.centerx, panel.top + 140), PAPER, self.font, center=True)
        self.text("Nethra's lantern gathering is ready to begin.", (panel.centerx, panel.top + 171), PAPER, self.font, center=True)
        footer = pygame.Rect(335, HEIGHT - 89, 482, 42)
        pygame.draw.rect(self.screen, (21, 54, 42), footer, border_radius=10)
        pygame.draw.rect(self.screen, GOLD, footer, 2, border_radius=10)
        self.text("R  Begin again      Q / ESC  Leave gathering", footer.center, WHITE, self.font, center=True)

    def draw_credits(self) -> None:
        self.screen.blit(self.loading_art, (0, 0))
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((12, 34, 26, 170))
        self.screen.blit(shade, (0, 0))
        panel = pygame.Rect(292, 100, 568, 500)
        pygame.draw.rect(self.screen, CREAM, panel, border_radius=16)
        pygame.draw.rect(self.screen, GOLD, panel, 3, border_radius=16)
        self.text("CREDITS", (panel.centerx, 156), GREEN, self.title, center=True)
        lines = [
            ("GOOD NEIGHBOURS", GREEN),
            ("A Little Town. A Lot of Kindness.", TERRACOTTA),
            ("", CHARCOAL),
            ("Developed by Arunez Zarro", CHARCOAL),
            ("", CHARCOAL),
            ("Programming & game design", CHARCOAL),
            ("Python + Pygame", CHARCOAL),
            ("Original generated game artwork", CHARCOAL),
            ("Ambient track supplied by the project creator", CHARCOAL),
        ]
        for index, (line, color) in enumerate(lines):
            self.text(line, (panel.centerx, 210 + index * 30), color, self.font if index < 2 else self.small, center=True)
        self.text("ESC / C / ENTER  Return to menu", (panel.centerx, 560), TERRACOTTA, self.font, center=True)

    def draw(self) -> None:
        if self.state == "LOADING":
            self.screen.blit(self.loading_art, (0, 0))
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((16, 42, 30, 120))
            self.screen.blit(shade, (0, 0))
            self.blit_scaled(self.logo_art, pygame.Rect(126, 82, 900, 300))
            self.text("A LITTLE TOWN. A LOT OF KINDNESS.", (WIDTH // 2, 400), WHITE, self.font, center=True)
            pygame.draw.rect(self.screen, PAPER, (WIDTH // 2 - 150, HEIGHT - 40, 300, 7), border_radius=4)
            pygame.draw.rect(self.screen, GOLD, (WIDTH // 2 - 150, HEIGHT - 40, int(300 * min(1, self.loading_elapsed / LOADING_SECONDS)), 7), border_radius=4)
        elif self.state == "MENU":
            # A distinct community-board menu, so it does not repeat the title loading card.
            self.draw_world()
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((20, 35, 25, 125))
            self.screen.blit(shade, (0, 0))
            board = pygame.Rect(126, 125, 430, 345)
            self.panel(board, CREAM)
            self.text("MAPLE STREET", (board.centerx, 175), GREEN, self.title, center=True)
            self.text("COMMUNITY BOARD", (board.centerx, 216), TERRACOTTA, self.font, center=True)
            self.text("Three neighbours are waiting for a little help.", (board.centerx, 270), CHARCOAL, self.small, center=True)
            self.text("ENTER / SPACE   Begin your afternoon", (board.centerx, 330), CHARCOAL, self.font, center=True)
            self.text("H   How to help", (board.centerx, 370), CHARCOAL, self.font, center=True)
            self.text("C   Credits", (board.centerx, 410), CHARCOAL, self.font, center=True)
            self.text("Q / ESC   Leave Maple Street", (board.centerx, 442), CHARCOAL, self.font, center=True)
            quote = self.menu_quotes[(pygame.time.get_ticks() // 4500) % len(self.menu_quotes)]
            self.text(quote, (WIDTH // 2, HEIGHT - 42), WHITE, self.font, center=True)
        elif self.state == "CREDITS":
            self.draw_credits()
        elif self.state == "VICTORY":
            self.draw_victory()
        elif self.state == "INTERIOR":
            self.draw_interior()
            self.draw_hud()
        else:
            self.draw_world()
            self.draw_hud()
            if self.state in ("HELP", "HELP_PLAY"):
                self.overlay("HOW TO HELP", ["Move: W A S D or arrow keys", "E: talk to neighbours or pick up items", "Complete all three requests to earn 30 Trust.", "H: this help screen   •   ESC / P: pause"], "Press H, ENTER, or ESC to return")
            elif self.state == "PAUSED":
                self.overlay("PAUSED", ["The afternoon is waiting for you.", "Open settings to adjust your soundtrack."], "ENTER / P / ESC Resume   •   S Settings   •   R Restart   •   Q Quit")
            elif self.state == "SETTINGS":
                self.draw_settings()
            elif self.state == "GAME_OVER":
                self.overlay("AFTERNOON HAS ENDED", [f"You earned {self.quests.trust} Community Trust today.", "Every neighbour will appreciate another visit tomorrow."], "R Try again   •   Q / ESC Quit")
        pygame.display.flip()

    def run(self) -> None:
        while True:
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)
            self.draw()


if __name__ == "__main__":
    Game().run()
