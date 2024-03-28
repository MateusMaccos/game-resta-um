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
@Pyro4.behavior(instance_mode='single')
class Jogo(object):
    def __init__(self):
        self.tabuleiro = [linha[:] for linha in tabuleiroInicial]
        # Tabuleiro para testar vencer
        # self.tabuleiro = [
        #     [-1, -1, 0, 0, 0, -1, -1],
        #     [-1, -1, 0, 0, 0, -1, -1],
        #     [1, 1, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 1, 1],
        #     [0, 0, 0, 1, 1, 0, 0],
        #     [-1, -1, 0, 0, 0, -1, -1],
        #     [-1, -1, 0, 0, 0, -1, -1],
        # ]
        self.jogadores = []
        self.estado_atual = "Esperando"
        self.turno_atual = None
        self.textos = []
    
    def pegar_adversario(self,id):
        if id == 'Jogador1':
            return 'Jogador2'
        else:
            return 'Jogador1'
    
    def pegar_estado_atual(self):
        return self.estado_atual
    
    def pegar_qntd_jogadores(self):
        return len(self.jogadores)

    def pegar_turno(self):
        return self.turno_atual
    
    def mudar_estado_atual(self,valor):
        self.estado_atual = valor

    def desconectou(self,id):
        self.jogadores.remove(id)
    
    def pegar_tabuleiro(self):
        return self.tabuleiro
    
    def pegar_chat(self):
        return self.textos
    
    def registrar_msg(self,id,msg):
        self.textos.append(id+":"+msg)

    def resetar_jogo_atual(self):
        self.tabuleiro = [linha[:] for linha in tabuleiroInicial]
        self.estado_atual = "Jogando"
        self.textos.clear()

    def registrar_jogador(self, id):
        if self.jogadores==[]:
            self.turno_atual=id
        self.jogadores.append(id)
        if len(self.jogadores)==2:
            self.estado_atual=="Jogando"

    def posicoesPossiveis(self, X, Y):
        posicoesPossiveis = []
        if (
            X + 1 != 7
            and self.tabuleiro[X + 1][Y] not in [0, -1]
            and X + 2 != 7
            and self.tabuleiro[X + 2][Y] == 0
        ):
            posicoesPossiveis.append([X + 2, Y])
        if (
            X - 1 != -1
            and self.tabuleiro[X - 1][Y] not in [0, -1]
            and X - 2 != -1
            and self.tabuleiro[X - 2][Y] == 0
        ):
            posicoesPossiveis.append([X - 2, Y])
        if (
            Y + 1 != 7
            and self.tabuleiro[X][Y + 1] not in [0, -1]
            and Y + 2 != 7
            and self.tabuleiro[X][Y + 2] == 0
        ):
            posicoesPossiveis.append([X, Y + 2])
        if (
            Y - 1 != -1
            and self.tabuleiro[X][Y - 1] not in [0, -1]
            and Y - 2 != -1
            and self.tabuleiro[X][Y - 2] == 0
        ):
            posicoesPossiveis.append([X, Y - 2])

        return posicoesPossiveis

    def moverPeca(self, inicial, final):
        self.tabuleiro[final[0]][final[1]] = 1
        self.tabuleiro[inicial[0]][inicial[1]] = 0
        if final[1] > inicial[1]:
            self.tabuleiro[final[0]][final[1] - 1] = 0
        elif final[1] < inicial[1]:
            self.tabuleiro[final[0]][final[1] + 1] = 0
        elif final[0] > inicial[0]:
            self.tabuleiro[final[0] - 1][final[1]] = 0
        elif final[0] < inicial[0]:
            self.tabuleiro[final[0] + 1][final[1]] = 0
        self.seu_turno = not self.seu_turno

    def verifica_fim_jogo(self):
        somador = sum([contador.count(1) for contador in self.tabuleiro])
        if somador == 1:
            self.estado_atual = "Fim"
        elif not self.existe_mov_possivel():
            self.estado_atual = "Empate"

    def existe_mov_possivel(self):
        for l in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[l])):
                if self.tabuleiro[l][c] == 1 and self.posicoesPossiveis(l, c) != []:
                    return True
        return False

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(Jogo)   # register the greeting maker as a Pyro object
ns.register("nome-server", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls
