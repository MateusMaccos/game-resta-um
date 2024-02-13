import pygame

# INICIANDO PROGRAMAÇÃO DO DISPLAY

# Resolução
LARGURA = 800
ALTURA = 525

display = pygame.display.set_mode((800, ALTURA))
pygame.display.set_caption("Jogo Resta Um")
pygame.font.init()
clock = pygame.time.Clock()

# CORES
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
COR_TABULEIRO = (204, 102, 0)


class Jogo:
    def __init__(self):
        self.tabuleiro = [
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
        ]
        self.turno = 0
        self.posicaoInicial = None
        self.posicaoFinal = None
        self.vencedor = None

    def avalia_posicao_clicada(self, coordenada):
        linha, coluna = linha_clicada(coordenada), coluna_clicada(coordenada)
        print(f"{linha},{coluna}")
        if self.posicaoInicial == None:
            self.posicaoInicial = [linha, coluna]
        else:
            movimentos = self.posicoesPossiveis(
                self.posicaoInicial[0], self.posicaoInicial[1]
            )
            print(movimentos)
            if [linha, coluna] in movimentos:
                print("entrou")
                self.posicaoFinal = [linha, coluna]
                self.moverPeca(self.posicaoInicial, self.posicaoFinal)
                self.posicaoInicial = None
                self.posicaoFinal = None
            else:
                self.posicaoInicial = [linha, coluna]
                self.posicaoFinal = None

    def desenha_tabuleiro(self):
        matriz = []
        for i in range(7):
            if i in [0, 1, 5, 6]:
                matriz.append([0, 0, 1, 1, 1, 0, 0])
            else:
                matriz.append([1, 1, 1, 1, 1, 1, 1])
        y = 0
        for l in range(len(matriz)):
            x = 0
            for c in range(len(matriz)):
                if matriz[l][c] == 0:
                    pygame.draw.rect(display, BRANCO, (x, y, 75, 75))
                else:
                    pygame.draw.rect(display, COR_TABULEIRO, (x, y, 75, 75))
                x += 75
            y += 75

        for l in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[l])):
                x = ALTURA / 7 * c + ALTURA / 14
                y = ALTURA / 7 * l + ALTURA / 14
                if self.tabuleiro[l][c] == 1:
                    pygame.draw.circle(display, BRANCO, (x, y), 20, 0)

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


def coluna_clicada(pos):
    x = pos[0]
    for i in range(1, 7):
        if x < i * (ALTURA) / 7:
            return i - 1
    return 6


def linha_clicada(pos):
    y = pos[1]
    for i in range(1, 7):
        if y < i * (ALTURA) / 7:
            return i - 1
    return 6


def loop_jogo():
    jogo = Jogo()
    sair = False
    while not sair:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair = True
                pygame.quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                jogo.avalia_posicao_clicada(pygame.mouse.get_pos())
        display.fill(PRETO)
        jogo.desenha_tabuleiro()
        pygame.display.update()
        clock.tick(60)


loop_jogo()
