import time
import sys
from can_bus import CANBus
from v2v_network import V2VNetwork
from messages.factory import create_message
from messages.types import MessageType

class CarNode:
    def __init__(self, car_id):
        self.car_id = car_id
        self.can = CANBus()
        self.v2v = V2VNetwork()

    def process_can(self):
        self.can.update()
        data = self.can.read()

        print(f"[{self.car_id}] CAN speed={data['speed']} brake={data['brake']}")

        if data["brake"]:
            self.send_v2v(
                MessageType.EMERGENCY_BRAKE,
                data
            )

        # Gửi định kỳ
        self.send_v2v(
            MessageType.SPEED_STATUS,
            {"speed": data["speed"]}
        )

        self.send_v2v(
            MessageType.POSITION_UPDATE,
            {"position": data["position"]}
        )


    def send_v2v(self, msg_type, payload):
        msg = create_message(
            sender=self.car_id,
            msg_type=msg_type,
            payload=payload
        )
        self.v2v.send(msg.to_dict())
        print(f"📤 {self.car_id} SEND {msg_type.value}")

    def process_v2v(self):
        msg = self.v2v.receive()
        if not msg or msg["sender"] == self.car_id:
            return

        msg_type = msg["type"]

        if msg_type == MessageType.EMERGENCY_BRAKE.value:
            print(f"⚠️ {self.car_id}: EMERGENCY BRAKE from {msg['sender']}")
            self.can.target_speed = max(0, self.can.speed - 20)

        elif msg_type == MessageType.SPEED_STATUS.value:
            print(f"ℹ️ {self.car_id}: SPEED from {msg['sender']}")

        elif msg_type == MessageType.POSITION_UPDATE.value:
            print(f"📍 {self.car_id}: POSITION update")

        elif msg_type == MessageType.LANE_CHANGE.value:
            print(f"↔️ {self.car_id}: LANE CHANGE")


    def run(self):
        print(f"🚗 {self.car_id} STARTED")
        while True:
            self.process_can()
            self.process_v2v()
            time.sleep(1)

if __name__ == "__main__":
    car_id = sys.argv[1] if len(sys.argv) > 1 else "Car_X"
    CarNode(car_id).run()
