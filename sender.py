import socket
import json
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

warning_msg = {
    "from": "Car_A",
    "type": "BRAKE",
    "priority": "HIGH",
    "message": "Phanh gấp! Có vật cản phía trước!"
}

print("🚗 Xe A đang chạy...")
time.sleep(3)

print("🚨 Xe A phát hiện vật cản → gửi cảnh báo!")
sock.sendto(json.dumps(warning_msg).encode(), (UDP_IP, UDP_PORT))

print("✅ Đã gửi cảnh báo V2V")
