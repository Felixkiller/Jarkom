import socket
import time

def udp_server():
    # Membuat socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Mengikat socket ke alamat IP dan port yang spesifik
    server_socket.bind(('localhost', 12000))

    print("Server is able to receive data now.")

    while True:
        # Menerima pesan dari klien
        message, client_address = server_socket.recvfrom(1024)

        # Mendapatkan waktu saat pesan diterima
        recv_time = time.time()

        # Menampilkan pesan yang diterima, alamat klien, dan waktu penerimaan
        print("The message received was '{}' from the address {} and the time was {}".format(message.decode(), client_address, recv_time))

        # Mengirimkan kembali pesan ke klien (echo server)
        server_socket.sendto(message, client_address)

# Titik masuk utama program
if __name__ == "__main__":
    udp_server()
