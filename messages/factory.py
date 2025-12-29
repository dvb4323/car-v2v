from .base import V2VMessage
from .types import MESSAGE_PRIORITY, MessageType


def create_message(sender, msg_type: MessageType, payload: dict):
    """
    Tạo V2V message theo type đã định nghĩa
    """
    priority = MESSAGE_PRIORITY[msg_type]
    return V2VMessage(
        sender=sender,
        msg_type=msg_type.value,
        priority=priority,
        payload=payload
    )
