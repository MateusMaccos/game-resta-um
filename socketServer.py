import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def receber_msg(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("Cliente: " + data.decode())


def enviar_msg(conn):
    while True:
        console = input()
        conn.sendall(console.encode())


def servidor(ip, porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, porta))
        s.listen()
        print(f"Esperando cliente")
        conn, addr = s.accept()
        with conn:
            print(f"Conectou em {addr}")
            thread_receber = threading.Thread(target=receber_msg(conn))
            thread_receber.start()
            enviar_msg(conn)


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
