from src.systems.quests import QuestManager


def test_each_quest_awards_trust_once() -> None:
    quests = QuestManager()

    assert quests.complete("can") is True
    assert quests.complete("can") is False
    assert quests.trust == 10
    assert quests.completed_count == 1


def test_three_quests_reach_victory() -> None:
    quests = QuestManager()

    for quest in ("can", "book", "groceries"):
        assert quests.complete(quest) is True

    assert quests.trust == 30
    assert quests.victory_reached is True


def test_unknown_quest_is_ignored() -> None:
    quests = QuestManager()

    assert quests.complete("not-a-quest") is False
    assert quests.trust == 0
