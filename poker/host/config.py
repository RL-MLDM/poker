class GameConfig:
    num_player: int
    num_hand: int

    def __init__(self, raw: dict):
        self.num_player = raw.get('room_number') or raw.get('num_player')
        self.num_hand = raw.get('game_number') or raw.get('num_hand')

    def __eq__(self, other: 'GameConfig'):
        return self.num_player == other.num_player \
               and self.num_hand == other.num_hand
