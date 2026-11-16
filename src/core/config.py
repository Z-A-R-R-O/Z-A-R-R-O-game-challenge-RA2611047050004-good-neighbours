"""Core configuration and palette definitions for Good Neighbours."""
from __future__ import annotations
import pygame

WIDTH, HEIGHT = 1152, 720
FPS = 60
WORLD = pygame.Rect(24, 92, WIDTH - 48, HEIGHT - 116)
PLAYER_SPEED = 220
AFTERNOON_SECONDS = 480
LOADING_SECONDS = 8.0

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
