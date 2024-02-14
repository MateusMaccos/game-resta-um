import pygame
import button

# INICIANDO PROGRAMAÇÃO DO DISPLAY

# Resolução
LARGURA = 1200
ALTURA = 800

display = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo Resta Um")
pygame.font.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont("arialblack", 40)
fontFina = pygame.font.SysFont("calibri", 40)
font_maior = pygame.font.SysFont("arialblack", 60)
background = pygame.image.load("images/menu.jpg")


def font_parametro(fonte, tamanho):
    return pygame.font.SysFont(fonte, tamanho)


# CORES
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
COR_TABULEIRO = (204, 102, 0)
COR_TABULEIRO_ESCURECIDO = (148, 74, 0)
VERDE = (100, 225, 0)
CINZA = (215, 215, 215)
CINZA_CLARO = (100, 100, 100)


def desenhar_background(tela, image):
    size = pygame.transform.scale(image, (1200, 800))
    display.blit(image, (0, 0))


def draw_text(tela, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    display.blit(img, (x, y))


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
        self.seu_turno = True
        self.posicaoInicial = None
        self.posicaoFinal = None
        self.estado_atual = "Jogando"

    def avalia_posicao_clicada(self, coordenada):
        linha, coluna = linha_clicada(coordenada), coluna_clicada(coordenada)
        if self.posicaoInicial == None:
            if self.tabuleiro[linha][coluna] == 1:
                self.posicaoInicial = [linha, coluna]
        else:
            movimentos = self.posicoesPossiveis(
                self.posicaoInicial[0], self.posicaoInicial[1]
            )
            if [linha, coluna] in movimentos:
                self.posicaoFinal = [linha, coluna]
                self.moverPeca(self.posicaoInicial, self.posicaoFinal)
                self.seu_turno = not self.seu_turno
                self.posicaoInicial = None
                self.posicaoFinal = None
            else:
                if self.tabuleiro[linha][coluna] == 1:
                    self.posicaoInicial = [linha, coluna]
                self.posicaoFinal = None

    def desenha_tabuleiro(self):
        matriz = []
        tamanho_quadrado = round(ALTURA / 7)
        raio_circulo = round(tamanho_quadrado / 3)
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
                    pygame.draw.rect(
                        display, BRANCO, (x, y, tamanho_quadrado, tamanho_quadrado)
                    )
                else:
                    pygame.draw.rect(
                        display,
                        COR_TABULEIRO,
                        (x, y, tamanho_quadrado, tamanho_quadrado),
                    )
                if self.posicaoInicial != None:
                    if [l, c] == [self.posicaoInicial[0], self.posicaoInicial[1]]:
                        pygame.draw.rect(
                            display,
                            COR_TABULEIRO_ESCURECIDO,
                            (x, y, tamanho_quadrado, tamanho_quadrado),
                        )
                    if [l, c] in self.posicoesPossiveis(
                        self.posicaoInicial[0], self.posicaoInicial[1]
                    ):
                        pygame.draw.rect(
                            display, VERDE, (x, y, tamanho_quadrado, tamanho_quadrado)
                        )
                x += tamanho_quadrado
            y += tamanho_quadrado

        for l in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[l])):
                x = ALTURA / 7 * c + ALTURA / 14
                y = ALTURA / 7 * l + ALTURA / 14
                if self.tabuleiro[l][c] == 1:
                    pygame.draw.circle(display, BRANCO, (x, y), raio_circulo, 0)

    def desenha_menu(self):
        if self.seu_turno:
            jogada = "Você"
        else:
            jogada = "Seu oponente"
        draw_text(
            display,
            f"Jogada:",
            fontFina,
            PRETO,
            ALTURA,
            0,
        )
        draw_text(
            display,
            jogada,
            font,
            COR_TABULEIRO,
            ALTURA,
            50,
        )

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

    def verifica_fim_jogo(self):
        somador = sum([contador.count(1) for contador in self.tabuleiro])
        if somador == 1:
            return "Fim"
        if not self.existe_mov_possivel():
            return "Empate"

    def existe_mov_possivel(self):
        for l in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[l])):
                if self.tabuleiro[l][c] == 1 and self.posicoesPossiveis(l, c) != []:
                    return True
        return False


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


def tela_fim_jogo(jogo, fim):
    sair = False
    while not sair:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair = True
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    sair = True

        display.fill(BRANCO)
        desenhar_background(display, background)
        draw_text(
            display,
            "Fim de jogo!",
            font,
            PRETO,
            480,
            300,
        )
        if fim == "Empate":
            draw_text(
                display,
                "Empate",
                font_maior,
                COR_TABULEIRO,
                480,
                400,
            )
        elif fim == "Fim":
            if jogo.seu_turno:
                mensagem = "Você"
                distancia = 400
            else:
                mensagem = "Seu oponente"
                distancia = 250
            draw_text(
                display,
                f"{mensagem} venceu!",
                font_maior,
                COR_TABULEIRO,
                distancia,
                400,
            )
        draw_text(
            display,
            "Aperte ESPAÇO para voltar para o início",
            font,
            PRETO,
            180,
            700,
        )
        pygame.display.update()
        clock.tick(60)


def criar_chat(textos, offset):
    PADDING = 110
    MARGIN = 50
    pygame.draw.rect(display, CINZA, (ALTURA, 120, LARGURA - ALTURA, ALTURA - 120))
    # chatFinal = []
    # inicio = len(textos) - 21
    # for i in range(inicio, len(textos)):
    #     chatFinal.append(textos[i])
    for texto in textos:
        # if len(texto)>20:
        posicao = ALTURA
        if texto.__contains__("Você"):
            text_surface = font_parametro("calibri", 30).render(
                texto, True, CINZA_CLARO
            )
        else:
            text_surface = font_parametro("calibri", 30).render(texto, True, PRETO)

        display.blit(text_surface, (posicao, offset + PADDING + MARGIN))

        MARGIN += text_surface.get_height()
    pygame.draw.rect(display, COR_TABULEIRO, (ALTURA, 120, LARGURA - ALTURA, 40))
    draw_text(
        display,
        "CHAT",
        font,
        BRANCO,
        ALTURA + 140,
        110,
    )
    pygame.draw.rect(display, BRANCO, (ALTURA, 0, LARGURA - ALTURA, 120))


def botoes_chat(offset):
    botao_subir_img = pygame.image.load("images/button_up.jpg")
    botao_descer_img = pygame.image.load("images/button_down.jpg")

    botao_subir_chat = button.Button(LARGURA - 20, 120, botao_subir_img, 1)
    botao_descer_chat = button.Button(LARGURA - 20, 140, botao_descer_img, 1)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    if botao_subir_chat.draw(display):
        offset += 5
    if botao_descer_chat.draw(display):
        offset -= 5
    return offset


def loop_jogo():
    jogo = Jogo()
    sair = False
    offset = 0
    textos = [
        "Oponente: ola",
        "Você: tudo bem?",
        "Oponente: blz?",
        "Oponente: blz?",
        "Oponente: blz?",
        "Oponente: blz?",
        "Oponente: blz?",
        "Oponente: blz?",
        "Oponente: blz?",
        "Oponente: blz?",
        "Oponente: blz?",
        "Oponente: blz?",
        "Oponente: blz?",
        "Você: tudo bem?",
        "Você: tudo bem?",
        "Você: tudo bem? eae? vai jogar?",
        "Você: tudo bem? eae? vai jogar?",
        "Você: tudo bem? eae? vai jogar?",
        "Você: tudo bem? eae? vai jogar?",
        "Você: tudo bem? eae? vai jogar?",
        "Você: tudo bem? eae? vai jogar?",
        "Você: tudo bem? eae? vai jogar?",
        "Você: tudo bem? eae? vai jogar?",
        "Você: tudo bem? eae? vai jogar?",
        "Você: tudo bem? eae? vai jogar?",
        "Você: tudo bem? eae? vai jogar?",
        "Você: tudo bem? eae? vai jogar?",
        "Você: tudo bem? eae? vai jogar?",
        "Você: tudo bem? eae? vai jogar?",
    ]
    while not sair:
        event_list = pygame.event.get()
        for evento in event_list:
            if evento.type == pygame.QUIT:
                sair = True
                pygame.quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                jogo.avalia_posicao_clicada(pygame.mouse.get_pos())
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    offset += 20
                if evento.key == pygame.K_DOWN:
                    offset -= 20

        display.fill(BRANCO)
        jogo.desenha_tabuleiro()
        criar_chat(textos, offset)
        offset = botoes_chat(offset)
        jogo.desenha_menu()

        fim_jogo = jogo.verifica_fim_jogo()
        if fim_jogo is not None:
            sair = True
            tela_fim_jogo(jogo, fim_jogo)

        pygame.display.update()
        clock.tick(60)


loop_jogo()
