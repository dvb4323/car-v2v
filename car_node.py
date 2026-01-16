import time
import sys
import threading
import select
from can_bus import CANBus
from v2v_network import V2VNetwork
from messages.factory import create_message
from messages.types import MessageType
from logger import log

class CarNode:
    def __init__(self, car_id):
        self.car_id = car_id
        self.can = CANBus()
        self.v2v = V2VNetwork()
        self.last_status_tx = 0.0
        self.running = True

    def process_can(self):
        self.can.update()
        data = self.can.read()

        log("CAN", f"speed={data['speed']} brake={data['brake']}", self.car_id)

        if data["brake"]:
            self.send_v2v(
                MessageType.EMERGENCY_BRAKE,
                data
            )

        # Gửi định kỳ
        if time.time() - self.last_status_tx > 1.0:
            self.send_v2v(
                MessageType.SPEED_STATUS,
                {"speed": data["speed"]}
            )
            self.send_v2v(
            MessageType.POSITION_UPDATE,
            {"position": data["position"]}
            )
            self.last_status_tx = time.time()

    def send_v2v(self, msg_type, payload):
        source = "MANUAL" if payload.get("manual") else "AUTO"
        msg = create_message(
            sender=self.car_id,
            msg_type=msg_type,
            payload=payload
        )
        self.v2v.send(msg.to_dict())
        log("V2V-TX", f"[{source}][{msg.priority.name}][{msg_type.value}] → broadcast", self.car_id)

    def process_v2v(self):
        msg = self.v2v.receive()
        if not msg or msg["sender"] == self.car_id:
            return

        msg_type = msg["type"]
        log("V2V-RX", f"[{msg['source']}][{msg['priority']}][{msg['type']}] ← {msg['sender']}", self.car_id)

        if msg_type == MessageType.EMERGENCY_BRAKE.value:
            log("DECISION", "priority=HIGH → ACTION=SLOW_DOWN", self.car_id)
            self.can.target_speed = max(0, self.can.speed - 20)

    def handle_user_command(self, cmd):
        log("INFO", f"MANUAL INPUT RECEIVED: '{cmd}'", self.car_id)
        cmd = cmd.strip().lower()

        if cmd == "b":
            self.can.brake = True
            self.send_v2v(
                MessageType.EMERGENCY_BRAKE,
                {"manual": True}
            )

        elif cmd == "s":
            self.send_v2v(
                MessageType.SPEED_STATUS,
                {"manual": True, "speed": self.can.speed}
            )

        elif cmd == "p":
            self.send_v2v(
                MessageType.POSITION_UPDATE,
                {"manual": True, "position": self.can.position}
            )

        elif cmd == "q":
            print("Exiting...")
            self.running = False


    def run(self):
        log("INFO", f"STARTED", self.car_id)
        
        while self.running:
            readable, _, _ = select.select([sys.stdin], [], [], 0)

            if readable:
                cmd = sys.stdin.readline().strip()
                if cmd:
                    self.handle_user_command(cmd)
                    
            self.process_can()
            self.process_v2v()
            time.sleep(1)

if __name__ == "__main__":
    car_id = sys.argv[1] if len(sys.argv) > 1 else "Car_X"
    CarNode(car_id).run()
