import json
from typing import List, Optional, Tuple

from poker.core import Card, ActionType, PlayerStatus, History


class State:
    position: int
    action_position: int
    legal_actions: List[ActionType]
    raise_range: Optional[Tuple[int, int]]
    private_card: List[Card]
    public_card: List[Card]
    players: List[PlayerStatus]
    history: List[List[History]]

    def __repr__(self):
        return json.dumps(self.json())

    def json(self) -> dict:
        return {
            'info': 'state',
            'position': self.position,
            'action_position': self.action_position,
            'legal_actions': [str(action_type) for action_type in self.legal_actions],
            'raise_range': list(self.raise_range) if self.raise_range else [],
            'private_card': [card.json() for card in self.private_card],
            'public_card': [card.json() for card in self.public_card],
            'players': [player.json() for player in self.players],
            'action_history': [[step.json() for step in stage] for stage in self.history]
        }

