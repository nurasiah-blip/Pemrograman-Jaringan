import socket
import select
import sys

def run_chat_client():
    server_host = '127.0.0.1'
    server_port = 9000

    # Buat socket client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    client_socket.setblocking(False)

    print("=== Terhubung ke Select Chat Server ===")
    print("Ketik pesan dan tekan ENTER (ketik 'bye' untuk keluar)")

    while True:
        # Socket yang dipantau: socket server & stdin (keyboard)
        sockets_list = [client_socket, sys.stdin]

        # Satpam OS: pantau socket & keyboard
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for sock in read_sockets:
            # KASUS 1: Pesan dari Server
            if sock == client_socket:
                try:
                    message = client_socket.recv(1024)
                    if not message:
                        print("[!] Server memutus koneksi.")
                        return
                    print(message.decode(), end='')
                except:
                    print("[!] Terjadi error koneksi.")
                    return

            # KASUS 2: Input dari Keyboard
            else:
                message = sys.stdin.readline()
                if message.strip().lower() == 'bye':
                    print("[!] Keluar dari chat.")
                    client_socket.close()
                    return
                client_socket.send(message.encode())

if __name__ == "__main__":
    sys.exit(run_chat_client())
