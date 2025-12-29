import random

class CANBus:
    def __init__(self):
        self.speed = random.randint(40, 80)
        self.brake = False
        self.position = random.randint(0, 100)
        self.target_speed = self.speed

    def update(self):
        # Random brake event
        self.brake = random.random() < 0.1

        # Nếu phanh → giảm target_speed
        if self.brake:
            self.target_speed = max(0, self.speed - 20)
        else:
            # Không phanh → quay lại tốc độ mong muốn
            self.target_speed = min(80, self.target_speed + 5)

        # Tiến dần về target_speed
        if self.speed < self.target_speed:
            self.speed += 5
        elif self.speed > self.target_speed:
            self.speed -= 10

    def read(self):
        return {
            "speed": self.speed,
            "brake": self.brake,
            "position": self.position
        }
