import socket
import json
import time
import random

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Agent berjalan... mengirim data")

while True:
    data = {
        "device_id": "AGENT-01",
        "cpu_usage": random.randint(10, 90),
        "temperature": random.randint(30, 60)
    }

    message = json.dumps(data)
    sock.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    print("Kirim:", message)
    time.sleep(2)
