from datetime import datetime


def log(channel, message, car_id=None):
    ts = datetime.now().strftime("%H:%M:%S")
    prefix = f"[{ts}] [{channel}]"
    if car_id:
        prefix += f" [{car_id}]"
    print(f"{prefix} {message}")
