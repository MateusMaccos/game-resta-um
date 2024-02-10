import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def receber_msg():
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("Cliente: " + data.decode())


def enviar_msg():
    while True:
        console = input()
        conn.sendall(console.encode())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Esperando cliente")
    conn, addr = s.accept()
    with conn:
        print(f"Conectou em {addr}")
        thread_receber = threading.Thread(target=receber_msg)
        thread_receber.start()
        enviar_msg()


# with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
#     s.bind((HOST, PORT))

#     print(f"Server UDP ouvindo")
#     while True:
#         bytesAddressPair = s.recvfrom(1024)

#         messagem = bytesAddressPair[0]

#         endereco = bytesAddressPair[1]

#         print("Cliente: " + messagem.decode())
#         if not messagem:
#             break
#         console = input()
#         s.sendto(console.encode(), endereco)
