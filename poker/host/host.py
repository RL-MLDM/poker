import socket

from poker.host.config import GameConfig
from poker.host.game import PokerGame
from poker.host.player import GamePlayer
from poker.host.utils import recv_json


class Host:
    socket: socket.socket

    def __init__(self, port, max_conn=233):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(port)
        self.socket.listen(max_conn)

    def __del__(self):
        self.socket.close()

    def _accept(self) -> socket:
        return self.socket.accept()[0]

    def run(self):
        while 1:
            master_conn = self._accept()
            master_raw = recv_json(master_conn)
            master_config = GameConfig(master_raw)
            game = PokerGame(master_config)
            room_full = game.add_player(GamePlayer(master_raw['name'], master_conn), master_config)

            while not room_full:
                sub_conn = self._accept()
                sub_raw = recv_json(sub_conn)
                sub_config = GameConfig(sub_raw)
                room_full = game.add_player(GamePlayer(sub_raw['name'], sub_conn), sub_config)

            game.start()
            del game
