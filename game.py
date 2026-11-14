"""GOOD NEIGHBOURS — a small, friendly Pygame adventure.

Run with: python game.py
"""
from __future__ import annotations

import sys
import pygame
from src.entities.world import Thing
from src.systems.quests import QuestManager

WIDTH, HEIGHT = 1152, 720
FPS = 60
WORLD = pygame.Rect(24, 92, WIDTH - 48, HEIGHT - 116)
PLAYER_SPEED = 220
AFTERNOON_SECONDS = 480

# Warm, readable palette.
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
        pygame.display.set_caption("GOOD NEIGHBOURS — A Little Town. A Lot of Kindness.")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 25)
        self.small = pygame.font.Font(None, 20)
        self.title = pygame.font.Font(None, 52)
        self.state = "MENU"
        self.reset()

    def reset(self) -> None:
        self.player = pygame.Rect(365, 550, 24, 28)
        self.quests = QuestManager()
        self.time_left = float(AFTERNOON_SECONDS)
        self.message = "Maple Street used to share every little thing. Today, a few kind errands can bring that warmth back."
        self.message_visible = 0.0
        self.dialogue_active = False
        self.speaker = "Maple Street"
        self.game_time = 0.0
        self.inventory: set[str] = set()
        self.walls = [
            pygame.Rect(155, 168, 170, 112), pygame.Rect(735, 168, 170, 112),
            pygame.Rect(155, 460, 165, 110), pygame.Rect(740, 460, 155, 125),
            pygame.Rect(448, 315, 200, 18), pygame.Rect(448, 315, 18, 130),
            pygame.Rect(630, 315, 18, 130),
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
            Thing("library book", pygame.Rect(840, 304, 24, 26), TERRACOTTA, "book"),
            Thing("groceries", pygame.Rect(410, 480, 28, 25), GOLD, "groceries"),
        ]
        self.entries = [
            Thing("Library", pygame.Rect(230, 270, 28, 18), GREEN, "enter_library"),
            Thing("Home", pygame.Rect(230, 568, 28, 18), GREEN, "enter_home"),
            Thing("Grocery", pygame.Rect(810, 270, 28, 18), GREEN, "enter_grocery"),
            Thing("Town Hall", pygame.Rect(810, 585, 28, 18), GREEN, "enter_hall"),
        ]

    def set_message(self, text: str, speaker: str | None = None) -> None:
        self.message, self.message_visible = text, 0.0
        self.dialogue_active = True
        if speaker is not None:
            self.speaker = speaker

    def move_player(self, dx: float, dy: float) -> None:
        self.player.x += round(dx)
        if self.player.left < WORLD.left or self.player.right > WORLD.right or any(self.player.colliderect(w) for w in self.walls):
            self.player.x -= round(dx)
        self.player.y += round(dy)
        if self.player.top < WORLD.top or self.player.bottom > WORLD.bottom or any(self.player.colliderect(w) for w in self.walls):
            self.player.y -= round(dy)

    def nearest(self) -> Thing | None:
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
            pygame.quit(); sys.exit()
        if event.type != pygame.KEYDOWN:
            return
        key = event.key
        if self.state == "MENU":
            if key in (pygame.K_RETURN, pygame.K_SPACE): self.state = "PLAYING"
            elif key in (pygame.K_q, pygame.K_ESCAPE): pygame.quit(); sys.exit()
        elif self.state == "PLAYING":
            if key == pygame.K_e:
                if self.dialogue_active:
                    if self.message_visible < len(self.message):
                        self.message_visible = float(len(self.message))
                    else:
                        self.dialogue_active = False
                else:
                    self.interact()
            elif key in (pygame.K_ESCAPE, pygame.K_p): self.state = "PAUSED"
            elif key == pygame.K_q: pygame.quit(); sys.exit()
        elif self.state == "PAUSED":
            if key in (pygame.K_ESCAPE, pygame.K_p, pygame.K_RETURN): self.state = "PLAYING"
            elif key == pygame.K_r: self.reset(); self.state = "PLAYING"
            elif key == pygame.K_q: pygame.quit(); sys.exit()
        elif self.state in ("VICTORY", "GAME_OVER"):
            if key == pygame.K_r: self.reset(); self.state = "PLAYING"
            elif key in (pygame.K_q, pygame.K_ESCAPE): pygame.quit(); sys.exit()

    def update(self, dt: float) -> None:
        if self.state != "PLAYING":
            return
        if self.dialogue_active:
            self.message_visible = min(len(self.message), self.message_visible + dt * 58)
            return
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        if dx or dy:
            length = max(1, (dx * dx + dy * dy) ** 0.5)
            self.move_player(dx / length * PLAYER_SPEED * dt, dy / length * PLAYER_SPEED * dt)
        self.time_left -= dt
        self.game_time += dt
        if self.quests.victory_reached: self.state = "VICTORY"
        elif self.time_left <= 0: self.state = "GAME_OVER"

    def draw(self) -> None:
        self.screen.fill(CREAM)
        if self.state == "PLAYING":
            pygame.draw.rect(self.screen, LIGHT_GREEN, WORLD)
            for wall in self.walls:
                pygame.draw.rect(self.screen, CHARCOAL, wall)
            for npc in self.npcs:
                pygame.draw.rect(self.screen, npc.color, npc.rect)
            for item in self.items:
                if item.kind not in self.inventory:
                    pygame.draw.rect(self.screen, item.color, item.rect)
            pygame.draw.rect(self.screen, TERRACOTTA, self.player)
            # HUD
            hud = self.font.render(f"Trust: {self.quests.trust}/30   Time: {int(self.time_left)}s", True, CHARCOAL)
            self.screen.blit(hud, (30, 30))
            if self.dialogue_active:
                pygame.draw.rect(self.screen, PAPER, pygame.Rect(100, HEIGHT - 120, WIDTH - 200, 90), border_radius=8)
                name = self.font.render(self.speaker, True, GREEN)
                self.screen.blit(name, (120, HEIGHT - 110))
                msg = self.small.render(self.message[:int(self.message_visible)], True, CHARCOAL)
                self.screen.blit(msg, (120, HEIGHT - 80))
        pygame.display.flip()

    def run(self) -> None:
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
