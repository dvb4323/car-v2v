from enum import Enum
from .base import Priority


class MessageType(Enum):
    EMERGENCY_BRAKE = "EMERGENCY_BRAKE"
    COLLISION_WARNING = "COLLISION_WARNING"
    SPEED_STATUS = "SPEED_STATUS"
    POSITION_UPDATE = "POSITION_UPDATE"
    LANE_CHANGE = "LANE_CHANGE"


# Mapping message → priority (giống bảng trong báo cáo)
MESSAGE_PRIORITY = {
    MessageType.EMERGENCY_BRAKE: Priority.HIGH,
    MessageType.COLLISION_WARNING: Priority.HIGH,
    MessageType.LANE_CHANGE: Priority.MEDIUM,
    MessageType.SPEED_STATUS: Priority.LOW,
    MessageType.POSITION_UPDATE: Priority.LOW,
}
