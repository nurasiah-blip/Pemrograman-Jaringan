import socket
import ssl

def run_secure_server():
    # 1. Konteks SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # Muat sertifikat & private key yang kita buat tadi
    context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")

    # 2. Socket Biasa
    bindsocket = socket.socket()
    bindsocket.bind(('localhost', 10023))
    bindsocket.listen(5)
    print("Secure Server listening on port 10023...")

    while True:
        try:
            newsocket, fromaddr = bindsocket.accept()
            print(f"[NEW] Koneksi TCP dari {fromaddr}")

            # 3. WRAP (Bungkus) Socket dengan SSL
            # Di sinilah proses Handshake terjadi
            conn = context.wrap_socket(newsocket, server_side=True)
            print(f"[SECURE] SSL Handshake sukses dengan {fromaddr}")

            # Komunikasi biasa (tapi terenkripsi otomatis)
            data = conn.recv(1024)
            print(f"Pesan (Decrypted): {data.decode()}")

            conn.send(b"Pesan Anda aman bersama kami.")

        except ssl.SSLError as e:
            print(f"[ERROR] Masalah SSL: {e}")
        except Exception as e:
            print(f"Error lain: {e}")
        finally:
            # conn.close()
            pass

if __name__ == "__main__":
    run_secure_server()