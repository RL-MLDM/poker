card_ranks = [
    '2', '3', '4', '5', '6', '7',
    '8', '9', 'T', 'J', 'Q', 'K', 'A'
]

card_suits = ['c', 'd', 's', 'h']

all_cards = [rank + suit for rank in card_ranks for suit in card_suits]

card_codes = {card: index for index, card in enumerate(all_cards, 1)}


class Card:
    rank: str
    suit: str

    def __init__(self, rank: str, suit: str):
        assert rank in card_ranks
        assert suit in card_suits
        self.rank = rank
        self.suit = suit

    def __eq__(self, other: 'Card'):
        return self.code == other.code

    def __str__(self):
        return self.rank_suit

    def __repr__(self):
        return self.rank_suit

    @property
    def code(self):
        return card_codes[self.rank + self.suit]

    @property
    def rank_suit(self):
        return self.rank + self.suit

    @property
    def suit_rank(self):
        return self.suit + self.rank

    @staticmethod
    def from_rank_suit(rank_suit: str) -> 'Card':
        rank = rank_suit[0].upper()
        suit = rank_suit[1].lower()
        return Card(rank, suit)

    @staticmethod
    def from_suit_rank(suit_rank: str) -> 'Card':
        rank = suit_rank[1].upper()
        suit = suit_rank[0].lower()
        return Card(rank, suit)

    def json(self) -> str:
        return self.rank_suit
