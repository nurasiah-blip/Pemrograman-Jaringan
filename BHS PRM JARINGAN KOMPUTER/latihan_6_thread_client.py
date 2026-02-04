import socket
import threading

# Konfigurasi Server
HOST = 'localhost'   # ganti IP server jika beda komputer
PORT = 5555

# Membuat socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("=== Terhubung ke Chat Room ===")

def receive_messages():
    """Thread untuk menerima pesan dari server"""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                print("[!] Koneksi ke server terputus.")
                break
            print(message)
        except:
            print("[!] Terjadi error saat menerima pesan.")
            client.close()
            break

def send_messages():
    """Thread untuk mengirim pesan ke server"""
    while True:
        try:
            message = input()
            client.send(message.encode('utf-8'))

            # Jika client ingin keluar
            if message.lower() == 'bye':
                client.close()
                break
        except:
            print("[!] Gagal mengirim pesan.")
            break

# Thread penerima pesan
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

# Thread pengirim pesan
send_messages()
