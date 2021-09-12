from socket import socket

from poker.host.utils import recv_json, send_json


class GamePlayer:
    name: str
    conn: socket

    def __init__(self, name: str, conn: socket):
        self.name = name
        self.conn = conn

    def recv(self) -> dict:
        return recv_json(self.conn)

    def send(self, data: dict):
        send_json(self.conn, data)
