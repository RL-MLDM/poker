from abc import ABC

from poker.core import Action, ActionType


class IaActionType(ActionType):
    FOLD = 1
    CHECK = 2
    CALL = 3
    RAISE = 4
    SMALL_BLIND = 5
    BIG_BLIND = 6

    def __str__(self):
        if self == IaActionType.FOLD:
            return 'fold'
        elif self == IaActionType.CHECK:
            return 'check'
        elif self == IaActionType.CALL:
            return 'call'
        elif self == IaActionType.RAISE:
            return 'raise'
        else:
            assert False

class IaAction(Action, ABC):
    @staticmethod
    def parse(raw: str) -> 'IaAction':
        if raw == 'fold':
            return IaFold()
        elif raw == 'call':
            return IaCall()
        elif raw == 'check':
            return IaCheck()
        elif raw[0] == 'r':
            return IaRaise(int(raw[1:]))
        else:
            raise ValueError(f'Invalid action string: {raw}')


class IaFold(IaAction):
    def __init__(self):
        super().__init__(IaActionType.FOLD)

    def __str__(self):
        return 'fold'

    def code(self) -> int:
        return 0


class IaCheck(IaAction):
    def __init__(self):
        super().__init__(IaActionType.CHECK)

    def __str__(self):
        return 'check'

    def code(self) -> int:
        return 1


class IaCall(IaAction):
    def __init__(self):
        super().__init__(IaActionType.CALL)

    def __str__(self):
        return 'call'

    def code(self) -> int:
        return 1


class IaRaise(IaAction):
    amount: int

    def __init__(self, amount: int):
        super().__init__(IaActionType.RAISE)
        self.amount = amount

    def __str__(self):
        return f'r{self.amount}'

    def __eq__(self, other: 'IaRaise'):
        return super().__eq__(other) \
               and self.amount == other.amount

    def code(self) -> int:
        return 2


class IaSmallBlind(IaAction):
    def __init__(self):
        super().__init__(IaActionType.SMALL_BLIND)

    def code(self) -> int:
        return -1


class IaBigBlind(IaAction):
    def __init__(self):
        super().__init__(IaActionType.BIG_BLIND)

    def code(self) -> int:
        return -1
