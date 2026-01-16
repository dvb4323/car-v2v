import socket
import json
from datetime import datetime

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("🚗 Xe B đang lắng nghe cảnh báo V2V...")

while True:
    data, addr = sock.recvfrom(1024)
    msg = json.loads(data.decode())

    timestamp = datetime.now().strftime("%H:%M:%S")

    print(f"\n[{timestamp}] 📩 Nhận cảnh báo từ {msg['from']}")
    print(f"   ▶ Loại: {msg['type']}")
    print(f"   ▶ Mức ưu tiên: {msg['priority']}")
    print(f"   ▶ Nội dung: {msg['message']}")

    if msg["priority"] == "HIGH":
        print("   ⚠️  CẢNH BÁO NGUY HIỂM! GIẢM TỐC ĐỘ!")
