import socket
import json

BROADCAST_IP = "255.255.255.255"
PORT = 5005

class V2VNetwork:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # ⭐ CHO PHÉP NHIỀU PROCESS DÙNG CHUNG PORT
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # ⭐ Linux hỗ trợ thêm (khuyến nghị)
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except AttributeError:
            pass

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.sock.bind(("", PORT))
        self.sock.setblocking(False)

    def send(self, msg_dict):
        self.sock.sendto(
            json.dumps(msg_dict).encode(),
            (BROADCAST_IP, PORT)
        )

    def receive(self):
        try:
            data, _ = self.sock.recvfrom(2048)
            return json.loads(data.decode())
        except BlockingIOError:
            return None
