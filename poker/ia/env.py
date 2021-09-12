import random
from copy import deepcopy
from typing import List, Optional, Tuple

from poker.ia.utils import get_winner
from poker.core import PlayerStatus, PlayerResult, Card, History, State, Result
from poker.core.card import all_cards
from poker.core.constants import INIT_STACK, SMALL_BLIND, BIG_BLIND
from poker.ia.action import IaActionType, IaAction, IaRaise, IaSmallBlind, IaBigBlind


class Env:
    player_names: List[str]
    players: List[PlayerStatus]
    history: List[List[History]]
    private_cards: List[List[Card]]
    public_card_all: List[Card]
    min_raise_by: int
    max_contribution: int
    stage_contribution: List[int]
    position: int
    folded: List[bool]

    def __init__(self, player_names: List[str]):
        self.player_names = player_names

    def reset(self):
        cards = [Card.from_rank_suit(card_r_s) for card_r_s in all_cards]
        random.shuffle(cards)

        self.players = [PlayerStatus(position=i, name=player_name, init_chip=INIT_STACK)
                        for i, player_name in enumerate(self.player_names)]
        self.history = []
        self.private_cards = [cards[i * 2:i * 2 + 2] for i in range(self.num_player)]
        self.public_card_all = cards[-5:]
        self.folded = [False] * self.num_player
        self.position = 0
        self.stage_contribution = [0] * self.num_player
        self.new_stage()
        self.small_blind()
        self.big_blind()

    def get_state(self, position: int) -> State:
        ret = State()
        ret.position = position
        ret.action_position = self.position
        ret.legal_actions, ret.raise_range = self._get_legal_actions()
        ret.private_card = self.private_cards[position]
        ret.public_card = self._get_public_card()
        ret.players = self.players
        ret.history = self.history
        return deepcopy(ret)

    def all_states(self) -> Tuple[str, State]:
        for i, player in enumerate(self.players):
            yield player.name, self.get_state(i)

    @property
    def result(self) -> Result:
        if not self.is_over():
            raise AssertionError('Current hand is running.')
        else:
            ret = Result()
            ret.private_card = [card_pair if not self.folded[i] else None for i, card_pair in
                                enumerate(self.private_cards)]
            ret.public_card = self._get_public_card()
            ret.players = [PlayerResult.from_status(self.players[i], win_chip) for i, win_chip in enumerate(self.win_chip)]
            ret.history = self.history
            return ret

    @property
    def num_player(self) -> int:
        return len(self.player_names)

    def new_stage(self):
        self.min_raise_by = 0
        self.max_contribution = 0
        self.position = 0 if self.curr_stage == -1 else 1
        self.stage_contribution = [0] * self.num_player
        self.history.append([])

    def new_action(self, action: IaAction):
        self._new_action(self.position, action)

    def _new_action(self, position: int, action: IaAction):
        if action.type == IaActionType.FOLD:
            self.folded[position] = True
            self._record(position, action)
        elif action.type == IaActionType.CHECK:
            self._record(position, action)
        elif action.type == IaActionType.CALL:
            call_by = self.max_contribution - self.stage_contribution[position]
            self.contribute(position, call_by)
            self._record(position, action)
        elif action.type == IaActionType.SMALL_BLIND:
            self.contribute(position, SMALL_BLIND)
            self.max_contribution = SMALL_BLIND
        elif action.type == IaActionType.BIG_BLIND:
            self.contribute(position, BIG_BLIND)
            self.max_contribution = BIG_BLIND
        elif action.type == IaActionType.RAISE:
            assert isinstance(action, IaRaise)
            raise_action: IaRaise = action
            raise_to = raise_action.amount
            raise_by = raise_to - self.max_contribution
            self.min_raise_by = raise_by
            self.max_contribution = raise_to
            self.contribute(position, raise_to - self.stage_contribution[position])
            self._record(position, action)
        else:
            assert False
        self._next_position()

    def small_blind(self):
        self._new_action(0, IaSmallBlind())

    def big_blind(self):
        self._new_action(1, IaBigBlind())

    def contribute(self, position, amount):
        self.players[position].contribution += amount
        self.stage_contribution[position] += amount

    def _next_position(self):
        self.position = (self.position + 1) % self.num_player
        if self.folded[self.position]:
            self._next_position()

    def is_over(self) -> bool:
        valid_contributions = [self.stage_contribution[i] for i, fold in enumerate(self.folded) if not fold]
        if len(valid_contributions) == 1:
            return True
        elif self.curr_stage == 3 and len(set(valid_contributions)) == 1:
            return True
        else:
            return False

    def is_stage_over(self) -> bool:
        valid_contributions = [self.stage_contribution[i] for i, fold in enumerate(self.folded) if not fold]
        if len(set(valid_contributions)) == 1:
            return True
        else:
            return False

    @property
    def win_chip(self) -> List[int]:
        valid_positions = [i for i, fold in enumerate(self.folded) if not fold]
        if len(valid_positions) == 1:
            winner_positions = valid_positions[:]
        else:
            winner_positions = get_winner(self.private_cards, self.public_card_all)

        winner_chip_avg = sum([player.contribution
                               for i, player in enumerate(self.players) if i not in winner_positions]
                              ) / len(winner_positions)
        return [winner_chip_avg if i in winner_positions else -player.contribution
                for i, player in enumerate(self.players)]

    @property
    def curr_stage(self):
        return len(self.history) - 1

    def _record(self, position: int, action: IaAction):
        self.history[-1].append(History(position, action))

    def _get_public_card(self) -> List[Card]:
        if self.curr_stage == 0:
            return []
        elif self.curr_stage == 1:
            return self.public_card_all[:3]
        elif self.curr_stage == 2:
            return self.public_card_all[:4]
        elif self.curr_stage == 3:
            return self.public_card_all[:5]
        else:
            assert False

    def _get_legal_actions(self) -> Tuple[List[IaActionType], Optional[Tuple[int, int]]]:
        legal_actions = [IaActionType.FOLD]
        if self.stage_contribution[self.position] < self.max_contribution:
            legal_actions.append(IaActionType.CALL)
        else:
            legal_actions.append(IaActionType.CHECK)

        raised = [history for history in self.history[-1] if history.action.type == IaActionType.RAISE]
        if len(raised) >= 4:
            raise_range = None
        else:
            legal_actions.append(IaActionType.RAISE)
            min_raise_to = max(BIG_BLIND, self.max_contribution + self.min_raise_by)
            max_raise_to = self.stage_contribution[self.position] + self.players[self.position].chip_left
            min_raise_to = min(min_raise_to, max_raise_to)
            raise_range = (min_raise_to, max_raise_to)
        return legal_actions, raise_range
