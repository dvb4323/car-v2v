import socket
import json
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

warning_msg = [
    {
        "from": "Car_A",
        "type": "BRAKE",
        "priority": "HIGH",
        "message": "Phanh gấp! Có vật cản phía trước!"
    },
    {
        "from": "Car_A",
        "type": "GPS",
        "priority": "LOW",
        "message": "Vật cản hệ thống GPS!"
    }
]
while True:
    print("🚗 Xe A đang chạy...")  
    print("Menu: \n")
    print("1. Phát hiện vật cản gửi cảnh báo!")
    print("2. Phát hiện vật cản gps cảnh báo!")
    print("3. Thoát")
    key = input("Nhấn phím để gửi thông tin cảnh báo cho xe...")
    match key:
        case "1": 
            print("🚨 Xe A phát hiện vật cản → gửi cảnh báo!")
            sock.sendto(json.dumps(warning_msg[0]).encode(), (UDP_IP, UDP_PORT))  
        case "2": 
            print("🚨 Xe A phát hiện vật cản gps cảnh báo!")
            sock.sendto(json.dumps(warning_msg[1]).encode(), (UDP_IP, UDP_PORT))
        case "3":
            break
        
    


