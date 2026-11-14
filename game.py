"""GOOD NEIGHBOURS — a small, friendly Pygame adventure.

Run with: python game.py
"""
from __future__ import annotations

import sys
import pygame

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
        self.time_left = float(AFTERNOON_SECONDS)
        self.game_time = 0.0
        # Solid buildings and fences: moving into one is safely blocked.
        self.walls = [
            pygame.Rect(155, 168, 170, 112), pygame.Rect(735, 168, 170, 112),
            pygame.Rect(155, 460, 165, 110), pygame.Rect(740, 460, 155, 125),
            pygame.Rect(448, 315, 200, 18), pygame.Rect(448, 315, 18, 130),
            pygame.Rect(630, 315, 18, 130),
            # Willow River is solid water; the central gap aligns with the bridge.
            pygame.Rect(976, 110, 108, 220), pygame.Rect(976, 400, 108, 250),
        ]

    def move_player(self, dx: float, dy: float) -> None:
        # Axis-separated collision lets the player slide naturally along walls.
        self.player.x += round(dx)
        if self.player.left < WORLD.left or self.player.right > WORLD.right or any(self.player.colliderect(w) for w in self.walls):
            self.player.x -= round(dx)
        self.player.y += round(dy)
        if self.player.top < WORLD.top or self.player.bottom > WORLD.bottom or any(self.player.colliderect(w) for w in self.walls):
            self.player.y -= round(dy)

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
            if key in (pygame.K_ESCAPE, pygame.K_p): self.state = "PAUSED"
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
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        if dx or dy:
            length = max(1, (dx * dx + dy * dy) ** 0.5)
            self.move_player(dx / length * PLAYER_SPEED * dt, dy / length * PLAYER_SPEED * dt)
        self.time_left -= dt
        self.game_time += dt
        if self.time_left <= 0:
            self.state = "GAME_OVER"

    def draw(self) -> None:
        self.screen.fill(CREAM)
        if self.state == "MENU":
            title = self.title.render("GOOD NEIGHBOURS", True, GREEN)
            self.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 3)))
            sub = self.font.render("Press SPACE or ENTER to explore Maple Street", True, CHARCOAL)
            self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        elif self.state == "PLAYING":
            pygame.draw.rect(self.screen, LIGHT_GREEN, WORLD)
            for wall in self.walls:
                pygame.draw.rect(self.screen, CHARCOAL, wall)
            pygame.draw.rect(self.screen, TERRACOTTA, self.player)
            # HUD
            timer_text = self.font.render(f"Afternoon: {int(self.time_left)}s", True, CHARCOAL)
            self.screen.blit(timer_text, (30, 30))
        elif self.state == "PAUSED":
            txt = self.title.render("PAUSED", True, CHARCOAL)
            self.screen.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        elif self.state == "GAME_OVER":
            txt = self.title.render("SUNSET HAS FALLEN", True, RED)
            self.screen.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
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
