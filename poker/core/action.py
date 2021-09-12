import abc
from enum import IntEnum


class ActionType(IntEnum):
    pass


class Action(metaclass=abc.ABCMeta):
    type: ActionType

    def __init__(self, action_type: ActionType):
        self.type = action_type

    def __eq__(self, other: 'Action'):
        return self.type == other.type

    def code(self) -> int:
        raise NotImplementedError

    @staticmethod
    def parse(raw: str) -> 'Action':
        raise NotImplementedError
