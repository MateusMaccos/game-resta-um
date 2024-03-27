# saved as greeting-server.py
import Pyro4

tabuleiroInicial = [
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, -1, 1, 1, 1, -1, -1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, -1, 1, 1, 1, -1, -1],
]

@Pyro4.expose
class Jogo(object):
    def __init__(self):
        self.tabuleiro = [linha[:] for linha in tabuleiroInicial]
    def pegar_tabuleiro(self):
        return self.tabuleiro
    def jogar(self,posicaoX,posicaoY):
        x = int(posicaoX)
        y = int(posicaoY)
        self.tabuleiro[x][y]=1

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(Jogo)   # register the greeting maker as a Pyro object
ns.register("nome-server", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls