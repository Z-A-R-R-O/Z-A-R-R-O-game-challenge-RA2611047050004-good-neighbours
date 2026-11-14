"""Quest progression and one-time Community Trust rewards."""
from __future__ import annotations

from dataclasses import dataclass, field


QUEST_ORDER = ("can", "book", "groceries")
QUEST_REWARD = 10


@dataclass
class QuestManager:
    """Owns mission states and prevents duplicate Community Trust rewards."""

    states: dict[str, str] = field(default_factory=lambda: {quest: "available" for quest in QUEST_ORDER})
    trust: int = 0

    def is_completed(self, quest: str) -> bool:
        return self.states.get(quest) == "completed"

    def complete(self, quest: str) -> bool:
        """Complete a known quest once and return whether a reward was granted."""
        if quest not in self.states or self.is_completed(quest):
            return False
        self.states[quest] = "completed"
        self.trust += QUEST_REWARD
        return True

    @property
    def completed_count(self) -> int:
        return sum(self.is_completed(quest) for quest in QUEST_ORDER)

    @property
    def victory_reached(self) -> bool:
        return self.trust >= QUEST_REWARD * len(QUEST_ORDER)
