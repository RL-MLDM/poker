class PlayerBase:
    name: str
    position: int
    init_chip: int

    def __init__(self, name: str = None, position: int = None, init_chip: int = None):
        self.name = name
        self.position = position
        self.init_chip = init_chip

    def __eq__(self, other: 'PlayerBase'):
        return self.name == other.name \
               and self.position == other.position \
               and self.init_chip == other.init_chip


class PlayerStatus(PlayerBase):
    contribution: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contribution = 0

    @property
    def chip_left(self):
        return self.init_chip - self.contribution

    def __eq__(self, other: 'PlayerStatus'):
        return super().__eq__(other) \
               and self.chip_left == other.chip_left

    def json(self) -> dict:
        return {
            'position': self.position,
            'money_left': self.chip_left,
            'total_money': self.init_chip,
            'name': self.name
        }


class PlayerResult(PlayerBase):
    win_chip: int

    @property
    def chip_left(self) -> int:
        return self.init_chip + self.win_chip

    def __eq__(self, other: 'PlayerResult'):
        return super().__eq__(other) \
            and self.win_chip == other.win_chip

    @classmethod
    def from_status(cls, status: PlayerStatus, win_chip: int) -> 'PlayerResult':
        inst = cls()
        inst.name = status.name
        inst.position = status.position
        inst.init_chip = status.init_chip
        inst.win_chip = win_chip
        return inst

    def json(self) -> dict:
        return {
            'position': self.position,
            'win_money': self.win_chip,
            'moneyLeft': self.chip_left,
            'totalMoney': self.init_chip,
            'name': self.name
        }
