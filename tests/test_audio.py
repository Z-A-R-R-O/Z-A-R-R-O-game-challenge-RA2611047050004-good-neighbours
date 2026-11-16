"""Unit tests for AudioManager isolated system."""
from pathlib import Path
import pygame

from src.systems.audio import AudioManager


def test_audio_manager_init_and_clamping() -> None:
    audio = AudioManager(default_volume=0.5)
    assert audio.volume == 0.5
    assert not audio.muted

    # Clamping high
    audio.change_volume(1.5)
    assert audio.volume == 1.0

    # Clamping low
    audio.change_volume(-2.0)
    assert audio.volume == 0.0
    assert audio.muted


def test_audio_manager_toggle_mute() -> None:
    audio = AudioManager(default_volume=0.4)
    assert not audio.muted

    # Toggle mute on
    muted = audio.toggle_mute()
    assert muted is True
    assert audio.muted is True

    # Toggle mute off
    muted = audio.toggle_mute()
    assert muted is False
    assert audio.muted is False


def test_audio_manager_defensive_start_with_missing_dir() -> None:
    audio = AudioManager(asset_dir=Path("non_existent_folder_xyz"))
    # Should not raise exception even if directory or file does not exist
    audio.start_ambient_music()
