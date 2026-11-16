import pygame

from game import Game, LOADING_SECONDS


def dismiss_dialogue(game: Game) -> None:
    game.dialogue_active = False
    game.message_visible = float(len(game.message))


def interact_at(game: Game, thing) -> None:
    game.player.center = thing.rect.center
    game.interact()
    dismiss_dialogue(game)


def test_loading_transitions_to_menu() -> None:
    game = Game()
    game.update(LOADING_SECONDS - 0.1)
    assert game.state == "LOADING"
    game.update(0.2)
    assert game.state == "MENU"
    pygame.quit()


def test_loading_screen_can_be_skipped() -> None:
    game = Game()
    assert game.state == "LOADING"
    skip_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    game.handle_event(skip_event)
    assert game.state == "MENU"
    pygame.quit()


def test_fresh_playthrough_reaches_victory() -> None:
    game = Game()
    game.update(LOADING_SECONDS + 0.1)
    game.state = "PLAYING"

    interact_at(game, next(item for item in game.items if item.kind == "can"))
    interact_at(game, next(npc for npc in game.npcs if npc.kind == "eleanor"))

    interact_at(game, next(entry for entry in game.entries if entry.kind == "enter_library"))
    interact_at(game, next(item for item in game.items if item.kind == "book"))
    game.player.center = (pygame.display.get_surface().get_width() // 2, 658)
    game.interact()
    dismiss_dialogue(game)
    interact_at(game, next(npc for npc in game.npcs if npc.kind == "leo"))

    interact_at(game, next(entry for entry in game.entries if entry.kind == "enter_grocery"))
    interact_at(game, next(item for item in game.items if item.kind == "groceries"))
    game.player.center = (pygame.display.get_surface().get_width() // 2, 658)
    game.interact()
    dismiss_dialogue(game)
    interact_at(game, next(npc for npc in game.npcs if npc.kind == "noah"))

    game.update(0)
    assert game.quests.trust == 30
    assert game.state == "VICTORY"
    pygame.quit()
