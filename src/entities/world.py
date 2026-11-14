"""Small data objects representing residents, pickups, and entrances."""
from __future__ import annotations

from dataclasses import dataclass
import pygame


@dataclass
class Thing:
    """An interactive object placed in a Pygame world."""

    name: str
    rect: pygame.Rect
    color: tuple[int, int, int]
    kind: str
