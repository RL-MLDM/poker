from typing import Dict

from poker.ia.action import IaAction
from poker.host.config import GameConfig
from poker.host.player import GamePlayer
from poker.ia.env import Env


class PokerGame:
    config: GameConfig
    players: Dict[str, GamePlayer]

    def __init__(self, config: GameConfig):
        self.config = config
        self.players = {}

    def __del__(self):
        for player in self.players.values():
            player.conn.close()

    def add_player(self, player: GamePlayer, config: GameConfig) -> bool:
        if config != self.config:
            raise ValueError(f'Player {player.name} claimed inconsistent game configuration.')
        if player.name in self.players.values():
            raise ValueError(f'Name {player.name} already exists.')
        self.players[player.name] = player
        return len(self.players) >= self.config.num_player

    def start(self):
        env = Env(list(self.players.keys()))
        for i in range(1, self.config.num_hand + 1):
            env.reset()
            while not env.is_over():
                for player_name, state in env.all_states():
                    self.players[player_name].send(state.json())
                action_player_name = env.players[env.position].name

                action_data = self.players[action_player_name].recv()
                if action_data.get('info') != 'action' or not action_data.get('action'):
                    raise ValueError(f'Player {action_player_name} sent invalid action.')
                action_raw = action_data.get('action')
                action = IaAction.parse(action_raw)
                env.new_action(action)
                if not env.is_over() and env.is_stage_over():
                    env.new_stage()

            for player in self.players.values():
                player.send(env.result.json())

            if i < self.config.num_hand:  # get ready
                for player in self.players.values():
                    ready_data = player.recv()
                    if ready_data.get('info') != 'ready' or ready_data.get('status') != 'start':
                        raise ValueError(f'Player {player.name} failed to get ready.')



