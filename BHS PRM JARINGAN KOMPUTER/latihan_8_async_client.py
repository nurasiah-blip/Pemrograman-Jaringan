import asyncio

async def tcp_client():
    # 1. Membuka koneksi ke server (ASYNC, non-blocking)
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888
    )

    print("=== Terhubung ke Async Server ===")

    try:
        while True:
            # 2. Ambil input user (blocking, tapi aman di client)
            message = input("Client > ")

            # Kirim pesan ke server
            writer.write((message + "\n").encode())
            await writer.drain()

            # Jika client ingin keluar
            if message.lower() == 'bye':
                print("[!] Client mengakhiri koneksi.")
                break

            # 3. Terima balasan dari server (ASYNC)
            data = await reader.read(100)
            if not data:
                print("[!] Server memutus koneksi.")
                break

            print(f"Server > {data.decode().strip()}")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        # 4. Tutup koneksi dengan rapi
        writer.close()
        await writer.wait_closed()
        print("=== Koneksi Ditutup ===")

if __name__ == "__main__":
    try:
        asyncio.run(tcp_client())
    except KeyboardInterrupt:
        print("\nClient Dihentikan.")
