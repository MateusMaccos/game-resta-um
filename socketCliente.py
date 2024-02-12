import socket
import threading

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


def receber_msg(s):
    while True:
        data = s.recv(1024)
        print("Servidor: " + data.decode())


def enviar_msg(s):
    while True:
        console = input()
        s.sendall(console.encode())


def cliente(ip, porta):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, int(porta)))
            # while True:
            #     console = input()
            #     s.sendall(console.encode())
            #     data = s.recv(1024)
            #     print("Servidor: " + data.decode())
            thread_receber = threading.Thread(target=receber_msg, args=(s,))
            thread_receber.start()
            enviar_msg(s)
    except:
        print("Não foi possivel conectar")


# with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
#     s.connect((HOST, PORT))
#     while True:
#         console = input()
#         s.sendto(console.encode(), (HOST, PORT))
#         data = s.recvfrom(1024)
#         print("Servidor: " + data[0].decode())
