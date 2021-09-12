import json
import struct
from typing import Optional


def recv_json(conn) -> Optional[dict]:
    data = conn.recv(4)
    if not data:
        return None
    length = struct.unpack('i', data)[0]
    data = conn.recv(length).decode('utf-8')
    while len(data) != length:
        data += conn.recv(length - len(data)).decode()
    return json.loads(data)


def send_json(conn, json_data: dict):
    data = json.dumps(json_data).encode('utf-8')
    conn.send(struct.pack('i', len(data)))
    conn.sendall(data)