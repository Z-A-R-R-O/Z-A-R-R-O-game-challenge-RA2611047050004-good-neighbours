"""Audio management system for ambient soundtrack and sound controls."""
from __future__ import annotations

from pathlib import Path
import pygame


class AudioManager:
    """Manages background music, volume clamping, and mute state defensively."""

    def __init__(self, asset_dir: Path | None = None, default_volume: float = 0.28) -> None:
        self.asset_dir = asset_dir or (Path(__file__).resolve().parent.parent.parent / "assets")
        self._volume = max(0.0, min(1.0, default_volume))
        self._muted = False

    @property
    def volume(self) -> float:
        return self._volume

    @volume.setter
    def volume(self, val: float) -> None:
        self._volume = max(0.0, min(1.0, val))
        self._muted = (self._volume == 0.0)
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(0.0 if self._muted else self._volume)

    @property
    def muted(self) -> bool:
        return self._muted

    @muted.setter
    def muted(self, val: bool) -> None:
        self._muted = val
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(0.0 if self._muted else self._volume)

    def start_ambient_music(self) -> None:
        """Play the approved ambient loop defensively."""
        track = self.asset_dir / "good_neighbours_bg.mp3"
        if not track.exists():
            track = self.asset_dir / "ambient.ogg"
        if not track.exists() or not pygame.mixer.get_init():
            return
        try:
            pygame.mixer.music.load(track)
            pygame.mixer.music.set_volume(0.0 if self._muted else self._volume)
            pygame.mixer.music.play(-1)
        except pygame.error:
            # Missing or invalid audio device must not crash the game.
            return

    def change_volume(self, delta: float) -> float:
        """Adjust volume by delta and clamp safely between 0.0 and 1.0."""
        self._volume = max(0.0, min(1.0, self._volume + delta))
        self._muted = (self._volume == 0.0)
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(0.0 if self._muted else self._volume)
        return self._volume

    def toggle_mute(self) -> bool:
        """Toggle mute state and update mixer volume."""
        self._muted = not self._muted
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(0.0 if self._muted else self._volume)
        return self._muted
