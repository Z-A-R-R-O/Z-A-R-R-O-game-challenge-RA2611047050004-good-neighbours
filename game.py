"""GOOD NEIGHBOURS — a small, friendly Pygame adventure.

Run with: python game.py
"""
from __future__ import annotations

import sys
import pygame

WIDTH, HEIGHT = 1152, 720
FPS = 60

# Warm, readable palette.
CREAM = (241, 233, 215)
PAPER = (230, 217, 184)
GREEN = (53, 94, 74)
CHARCOAL = (38, 51, 45)


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("GOOD NEIGHBOURS — A Little Town. A Lot of Kindness.")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = "MENU"
        self.font = pygame.font.Font(None, 25)
        self.title = pygame.font.Font(None, 52)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_q, pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        self.screen.fill(CREAM)
        title = self.title.render("GOOD NEIGHBOURS", True, GREEN)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 3)))
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
