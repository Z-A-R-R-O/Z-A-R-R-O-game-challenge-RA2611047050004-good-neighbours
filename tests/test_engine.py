"""Tests for core engine mechanics: collision, boundaries, audio, and lifecycle."""
import pygame
from game import Game, WORLD, AFTERNOON_SECONDS


def test_player_collision_blocks_movement() -> None:
    game = Game()
    wall = game.walls[0]  # First building
    # Position player right against the right side of the wall
    game.player.topleft = (wall.right, wall.top + 10)
    initial_x = game.player.x

    # Attempt to move left into the wall
    game.move_player(-20, 0)
    assert game.player.x == initial_x
    assert not game.player.colliderect(wall)
    pygame.quit()


def test_player_clamped_within_world_boundaries() -> None:
    game = Game()
    # Position player inside, near the top-left corner
    game.player.topleft = (WORLD.left + 5, WORLD.top + 5)
    game.move_player(-10, -10)
    assert game.player.left >= WORLD.left
    assert game.player.top >= WORLD.top

    # Position player inside, near the bottom-right corner
    game.player.bottomright = (WORLD.right - 5, WORLD.bottom - 5)
    game.move_player(10, 10)
    assert game.player.right <= WORLD.right
    assert game.player.bottom <= WORLD.bottom
    pygame.quit()


def test_afternoon_countdown_triggers_game_over() -> None:
    game = Game()
    game.state = "PLAYING"
    # Advance time beyond the afternoon duration
    game.update(AFTERNOON_SECONDS + 1.0)
    assert game.state == "GAME_OVER"
    assert game.time_left <= 0
    pygame.quit()


def test_audio_controls_clamping_and_mute() -> None:
    game = Game()
    # Test volume clamping to maximum 1.0
    game.change_music_volume(2.0)
    assert game.music_volume <= 1.0

    # Test volume clamping to minimum 0.0
    game.change_music_volume(-5.0)
    assert game.music_volume == 0.0

    # Test mute toggling
    initial_mute = game.music_muted
    game.toggle_music()
    assert game.music_muted != initial_mute
    game.toggle_music()
    assert game.music_muted == initial_mute
    pygame.quit()


def test_collected_items_not_available_for_duplicate_pickup() -> None:
    game = Game()
    can = next(item for item in game.items if item.kind == "can")
    game.player.center = can.rect.center
    assert game.nearest() is not None

    # Pick up the watering can
    game.interact()
    assert "can" in game.inventory

    # Once carried, the can should no longer appear as an available nearby pickup
    nearest_thing = game.nearest()
    if nearest_thing is not None:
        assert nearest_thing.kind != "can"
    pygame.quit()


def test_pause_and_restart_lifecycle() -> None:
    game = Game()
    game.state = "PLAYING"
    game.quests.complete("can")
    assert game.quests.trust == 10

    # Press ESC to pause
    pause_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
    game.handle_event(pause_event)
    assert game.state == "PAUSED"

    # Press R to restart
    restart_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)
    game.handle_event(restart_event)
    assert game.state == "PLAYING"
    assert game.quests.trust == 0  # Fresh playthrough reset
    assert len(game.inventory) == 0
    pygame.quit()
