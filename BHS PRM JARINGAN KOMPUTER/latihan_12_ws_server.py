import asyncio
import websockets # pyright: ignore[reportMissingImports]
import json
import random

# Menyimpan semua client yang terhubung
CONNECTED_CLIENTS = set()

async def stock_handler(websocket):
    """
    Handler ini dijalankan setiap kali ada client baru connect
    """
    # 1. Register Client
    print("[NEW] Client bergabung.")
    CONNECTED_CLIENTS.add(websocket)

    try:
        # Kirim pesan selamat datang
        await websocket.send(json.dumps({"msg": "Welcome to Stock Ticker!"}))

        # Keep connection alive (looping listening)
        # Sebenarnya server kita tipe BROADCASTER (satu arah), 
        # tapi kita perlu loop agar koneksi tidak putus.
        async for message in websocket:
            print(f"Client sent: {message}")

    except websockets.exceptions.ConnectionClosed:
        print("[CLOSED] Client terputus.")
    finally:
        # 2. Unregister Client saat putus
        CONNECTED_CLIENTS.remove(websocket)

async def broadcast_price():
    """
    Fungsi latar belakang untuk generate harga palsu
    """
    while True:
        # Simulasi harga saham
        price_data = {
            "symbol": "BBCA",
            "price": random.randint(8000, 8500),
            "timestamp": "Live"
        }

        # Serialisasi ke JSON
        message = json.dumps(price_data)

        # Kirim ke SEMUA client yang ada di set
        if CONNECTED_CLIENTS:
            # websockets.broadcast butuh list/set client
            websockets.broadcast(CONNECTED_CLIENTS, message)
            print(f"[BROADCAST] {message} -> ke {len(CONNECTED_CLIENTS)} clients")

        await asyncio.sleep(1) # Update tiap 1 detik

async def main():
    # Jalankan server di port 6789
    async with websockets.serve(stock_handler, "localhost", 6789):
        print("=== WebSocket Server running on ws://localhost:6789 ===")

        # Jalankan broadcaster di background
        await broadcast_price() # Ini akan looping selamanya

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server Stopped.")