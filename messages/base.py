from enum import IntEnum
import time


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class V2VMessage:
    def __init__(self, sender, msg_type, priority, payload):
        self.sender = sender
        self.msg_type = msg_type
        self.priority = priority
        self.payload = payload
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "sender": self.sender,
            "type": self.msg_type,
            "priority": int(self.priority),
            "payload": self.payload,
            "timestamp": self.timestamp,
        }
