from poker.core import Action


class History:
    position: int
    action: Action

    def __init__(self, position: int, action: Action):
        self.position = position
        self.action = action

    def json(self) -> dict:
        return {
            'position': self.position,
            'action': str(self.action),
            'timestamp': ''
        }
