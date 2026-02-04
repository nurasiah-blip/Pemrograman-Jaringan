import socket

# Persiapan Socket Client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Hubungkan ke Server (alamat & port HARUS sama dengan server)
client.connect(('localhost', 5000))
print("=== Terhubung ke Chat Server ===")

# INTI CHAT: Loop komunikasi
while True:
    try:
        # 1. Kirim Pesan ke Server
        message = input("Client (Anda) > ")
        client.send(message.encode('utf-8'))

        # 2. Cek jika Client ingin keluar
        if message.lower() == 'bye':
            print("[!] Anda mengakhiri sesi.")
            break

        # 3. Terima Balasan dari Server (BLOCKING)
        reply = client.recv(1024).decode('utf-8')

        # Jika server memutus koneksi
        if not reply or reply.lower() == 'bye':
            print("[!] Server mengakhiri sesi.")
            break

        print(f"Server > {reply}")

    except Exception as e:
        print(f"Error Terjadi: {e}")
        break

# Bersih-bersih koneksi
client.close()
print("=== Aplikasi Client Ditutup ===")
