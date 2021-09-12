from typing import Dict, Any, List

from poker.ia.action import IaActionType, IaFold, IaCheck, IaCall, IaRaise
from poker.poker.constants import INIT_STACK
from poker.poker import State, Card, PlayerStatus, ActionType, History, Action, Result, PlayerResult


def __get_action(action: str) -> Action:
    if action == 'fold':
        return IaFold()
    elif action == 'check':
        return IaCheck()
    elif action == 'call':
        return IaCall()
    else:
        amount: int = int(action[1:])
        return IaRaise(amount)


def get_history_item(history: Dict[str, Any]) -> History:
    return History(history['position'], __get_action(history['action']), history['timestamp'])


def get_action_history(action_history: List[List[Dict[str, Any]]]) -> List[List[History]]:
    return [
        [get_history_item(item) for item in stage]
        for stage in action_history
    ]


class ResultBuilder:
    @classmethod
    def build(cls, recv: Dict[str, Any]) -> Result:
        result = Result()
        result.hand_cards = [
            [Card.from_rank_suit(card) for card in cards] if cards else None
            for cards in recv['player_card']
        ]
        result.public_card = [Card.from_rank_suit(card) for card in recv['public_card']]
        result.players = [cls.__get_player(player) for player in recv['players']]
        result.history = get_action_history(recv['action_history'])
        return result

    @classmethod
    def __get_player(cls, player: Dict[str, Any]) -> PlayerResult:
        player_result = PlayerResult()
        player_result.init_chip = INIT_STACK
        player_result.name = player['name']
        player_result.position = player['position']
        player_result.win_chip = player['win_money']
        return player_result


class StateBuilder:
    @classmethod
    def build(cls, recv: Dict[str, Any]) -> State:
        state = State()
        state.position = recv['position']
        state.players = [cls.__get_player(player) for player in recv['players']]
        state.hand_card = [Card.from_rank_suit(card) for card in recv['private_card']]
        state.public_card = [Card.from_rank_suit(card) for card in recv['public_card']]
        state.legal_actions = cls.__get_legal_actions(recv['legal_actions'])
        if IaActionType.RAISE in state.legal_actions:
            state.raise_range = (recv['raise_range'][0], recv['raise_range'][1])
        else:
            state.raise_range = None
        state.action_history = get_action_history(recv['action_history'])
        return state

    @classmethod
    def __get_player(cls, player: Dict[str, Any]) -> PlayerStatus:
        player_status = PlayerStatus()
        player_status.init_chip = INIT_STACK
        player_status.name = player['name']
        player_status.position = player['position']
        player_status.contribution = INIT_STACK - player['money_left']
        return player_status

    @classmethod
    def __get_legal_actions(cls, legal_actions: List[str]) -> List[ActionType]:
        ret: List[ActionType] = []
        if "fold" in legal_actions:
            ret.append(IaActionType.FOLD)
        if "check" in legal_actions:
            ret.append(IaActionType.CHECK)
        if "call" in legal_actions:
            ret.append(IaActionType.CALL)
        if "raise" in legal_actions:
            ret.append(IaActionType.RAISE)
        return ret
