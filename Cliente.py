# saved as greeting-client.py
import Pyro4

jogo = Pyro4.Proxy("PYRONAME:nome-server")    # use name server object lookup uri shortcut
while(True):
    X = input("Digite a posicao X: ").strip()
    Y = input("Digite a posicao Y: ").strip()
    jogo.jogar(X,Y)
    tabuleiro=jogo.pegar_tabuleiro()
    print(tabuleiro)
    