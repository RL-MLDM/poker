from typing import List, Optional

from poker.core import Card, PlayerResult, History


class Result:
    private_card: List[Optional[List[Card]]]
    public_card: List[Card]
    players: List[PlayerResult]
    history: List[List[History]]

    @property
    def win_money(self):
        return {player.name: player.win_chip for player in self.players}

    def json(self):
        return {
            'info': 'result',
            'player_card': [[card.json() for card in cards] if cards else None for cards in self.private_card],
            'public_card': [card.json() for card in self.public_card],
            'players': [player.json() for player in self.players],
            'action_history': [[step.json() for step in stage] for stage in self.history]
        }
