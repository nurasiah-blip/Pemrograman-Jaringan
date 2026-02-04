import socket
import json
import threading
import asyncio
import websockets

latest_data = {}

# ================= UDP SERVER =================
def udp_server():
    global latest_data
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 9999))
    print("✅ UDP Server aktif di port 9999")

    while True:
        data, addr = sock.recvfrom(1024)
        latest_data = json.loads(data.decode())
        print("📥 Data diterima:", latest_data)

# ================= WEBSOCKET =================
async def ws_handler(websocket):
    print("🌐 Client WebSocket terhubung")
    try:
        while True:
            if latest_data:
                await websocket.send(json.dumps(latest_data))
            await asyncio.sleep(1)
    except:
        print("❌ Client WebSocket terputus")

# ================= MAIN ASYNC =================
async def main():
    server = await websockets.serve(ws_handler, "localhost", 6789)
    print("✅ WebSocket Server aktif di ws://localhost:6789")
    await server.wait_closed()

# ================= RUN =================
if __name__ == "__main__":
    # Jalankan UDP di thread terpisah
    threading.Thread(target=udp_server, daemon=True).start()

    # Jalankan WebSocket (ASYNC, PYTHON 3.14 SAFE)
    asyncio.run(main())
