# Configurações iniciais
import pygame
import socket
import threading

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
programIcon = pygame.image.load("images/icone.png")
tabuleiroInicial = [
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, -1, 1, 1, 1, -1, -1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, -1, 1, 1, 1, -1, -1],
]

pygame.display.set_icon(programIcon)


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


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font, limiteCaracteres=42):
        super().__init__()
        self.limiteCaracteres = limiteCaracteres
        self.color = (255, 255, 255)
        self.backcolor = (0, 0, 0)
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface(
            (max(self.width, t_surf.get_width() + 10), t_surf.get_height() + 10),
            pygame.SRCALPHA,
        )
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(
            self.image, self.color, self.image.get_rect().inflate(-2, -2), 2
        )
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < self.limiteCaracteres:
                        self.text += event.unicode
                self.render_text()


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale))
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.cursor_changed = False  # Variável para controlar a alteração do cursor

    def draw(self, surface):
        action = False
        if self.is_hovered():
            if not self.cursor_changed:  # Verifica se o cursor já foi alterado
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.cursor_changed = True  # Marca que o cursor foi alterado
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.clicked = True
                action = True
        else:
            if (
                self.cursor_changed
            ):  # Se o cursor foi alterado antes e saiu do botão, restaura o cursor padrão
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.cursor_changed = False  # Marca que o cursor foi restaurado

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


def desenhar_background(tela, image):
    pygame.transform.scale(image, (1200, 800))
    tela.blit(image, (0, 0))


def draw_text(tela, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    tela.blit(img, (x, y))


class Jogo:
    def __init__(self):
        self.tabuleiro = tabuleiroInicial
        self.seu_turno = True
        self.posicaoInicial = None
        self.posicaoFinal = None
        self.estado_atual = "Jogando"
        self.socketAtual = None
        global textos
        textos = []

    def resetar_jogo_atual(self):
        self.tabuleiro = tabuleiroInicial
        self.seu_turno = True
        self.posicaoInicial = None
        self.posicaoFinal = None
        self.estado_atual = "Jogando"
        textos.clear()
        if self.socketAtual == "cliente":
            self.seu_turno = False
        else:
            self.seu_turno = True

    def resetar_jogo_adversario(self):
        if self.socketAtual == "cliente":
            cliente.enviar_mensagem("reiniciar")
        else:
            server.enviar_mensagem("reiniciar")

    def definir_socket(self, tipo):
        self.socketAtual = tipo
        if tipo == "cliente":
            self.seu_turno = False
        else:
            self.seu_turno = True

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
                if self.socketAtual == "cliente":
                    cliente.enviar_mensagem(
                        f"jogada:({self.posicaoInicial[0]},{self.posicaoInicial[1]})({self.posicaoFinal[0]},{self.posicaoFinal[1]})"
                    )
                else:
                    server.enviar_mensagem(
                        f"jogada:({self.posicaoInicial[0]},{self.posicaoInicial[1]})({self.posicaoFinal[0]},{self.posicaoFinal[1]})"
                    )
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
        self.seu_turno = not self.seu_turno

    def verifica_fim_jogo(self):
        somador = sum([contador.count(1) for contador in self.tabuleiro])
        if somador == 1:
            jogo.estado_atual = "Fim"
        elif not self.existe_mov_possivel():
            jogo.estado_atual = "Empate"

    def existe_mov_possivel(self):
        for l in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[l])):
                if self.tabuleiro[l][c] == 1 and self.posicoesPossiveis(l, c) != []:
                    return True
        return False


class Server:
    def __init__(self):
        self.conectado = False
        self.endereco = None
        self.connection = None
        self.encerrar = False
        self.socket = None

    def run(self, ip, porta):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip, porta))
            s.listen()
            self.socket = s
            print(f"Esperando cliente")
            try:
                conn, addr = s.accept()
            except:
                print("Deu ruim")

            with conn:
                self.endereco = addr
                self.conectado = True
                self.connection = conn
                print(f"Conectou em {addr}")
                thread_receber = threading.Thread(
                    target=receber_msg,
                    args=(conn,),
                )
                thread_receber.start()
                thread_receber.join()

    def encerrarConexao(self):
        self.encerrar = True
        self.conectado = False
        if self.connection:
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except Exception as e:
                print(f"Erro ao encerrar conexão: {e}")

    def enviar_mensagem(self, msg):
        enviar_msg(self.connection, msg)


class Cliente:
    def __init__(self):
        self.conectado = False
        self.connection = None
        self.error = False
        self.encerrar = None

    def run(self, ip, porta):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, int(porta)))
                self.conectado = True
                self.connection = s
                thread_receber = threading.Thread(
                    target=receber_msg,
                    args=(s,),
                )
                thread_receber.start()
                thread_receber.join()
        except ConnectionRefusedError:
            print("A conexão foi recusada pelo servidor.")
            self.conectado = False
            self.error = "A conexão foi recusada pelo servidor."
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            self.conectado = False
            self.error = "Não foi possível acessar a sala indicada"

    def encerrarConexao(self):
        self.encerrar = True
        self.conectado = False
        if self.connection:
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except Exception as e:
                print(f"Erro ao encerrar conexão: {e}")

    def enviar_mensagem(self, msg):
        enviar_msg(self.connection, msg)


def coluna_clicada(pos):
    x = pos[0]
    for i in range(1, 7):
        if x < i * (ALTURA) / 7:
            return i - 1
    if x > ALTURA:
        return -1
    return 6


def linha_clicada(pos):
    y = pos[1]
    for i in range(1, 7):
        if y < i * (ALTURA) / 7:
            return i - 1
    if y > ALTURA:
        return -1
    return 6


def tela_fim_jogo():
    sair = False
    reiniciar_img = pygame.image.load("images/botao_reiniciar.jpg")
    botao_reiniciar = Button(510, 550, reiniciar_img, 1)
    while not sair:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair = True
                if jogo.estado_atual != "Desconectou":
                    if jogo.socketAtual == "cliente":
                        cliente.encerrar = True
                        cliente.enviar_mensagem("desconectou")
                        cliente.encerrarConexao()
                    else:
                        server.encerrar = True
                        server.enviar_mensagem("desconectou")
                        server.encerrarConexao()
                return True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    sair = True
                    if jogo.estado_atual != "Desconectou":
                        if jogo.socketAtual == "cliente":
                            cliente.encerrar = True
                            cliente.enviar_mensagem("desconectou")
                            cliente.encerrarConexao()
                        else:
                            server.encerrar = True
                            server.enviar_mensagem("desconectou")
                            server.encerrarConexao()
                    return True

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
        if jogo.estado_atual in ["Empate", "Fim", "Reiniciar"]:
            if botao_reiniciar.draw(display):
                jogo.resetar_jogo_atual()
                jogo.resetar_jogo_adversario()
                return False
            if jogo.estado_atual == "Reiniciar":
                jogo.resetar_jogo_atual()
                return False
        if jogo.estado_atual == "Empate":
            draw_text(
                display,
                "Empate",
                font_maior,
                COR_TABULEIRO,
                480,
                400,
            )
        elif jogo.estado_atual == "Fim":
            if not jogo.seu_turno:
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
        elif jogo.estado_atual in ["Desistencia", "Desistiu"]:
            if jogo.estado_atual == "Desistiu":
                mensagem = "Você desistiu!"
                distancia = 400
            else:
                mensagem = "Seu oponente desistiu!"
                distancia = 250
            draw_text(
                display,
                f"{mensagem}",
                font_maior,
                COR_TABULEIRO,
                distancia,
                400,
            )
        elif jogo.estado_atual == "Desconectou":
            mensagem = "Seu oponente desconectou!"
            distancia = 200
            draw_text(
                display,
                f"{mensagem}",
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
    PADDING = ALTURA - 115
    MARGIN = 50
    pygame.draw.rect(display, CINZA, (ALTURA, 120, LARGURA - ALTURA, ALTURA - 120))
    cor = None
    for texto in reversed(textos):
        posicao = ALTURA
        if texto.__contains__("Você"):
            text_surface = font_parametro("calibri", 30).render(
                texto, True, CINZA_CLARO
            )
        elif texto.__contains__("Oponente"):
            text_surface = font_parametro("calibri", 30).render(texto, True, PRETO)
        else:
            if textos[textos.index(texto) - 1].__contains__("Você"):
                cor = CINZA_CLARO
            else:
                cor = PRETO
            text_surface = font_parametro("calibri", 30).render(texto, True, cor)
        display.blit(text_surface, (posicao, offset + PADDING + MARGIN))

        MARGIN -= text_surface.get_height()
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

    botao_subir_chat = Button(LARGURA - 20, 120, botao_subir_img, 1)
    botao_descer_chat = Button(LARGURA - 20, 140, botao_descer_img, 1)
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    if botao_subir_chat.draw(display):
        offset += 5
    if botao_descer_chat.draw(display):
        offset -= 5
    return offset


def loop_jogo(tipo):
    global jogo
    jogo = Jogo()
    jogo.definir_socket(tipo)
    sair = False
    offset = 0
    textField = TextInputBox(
        ALTURA, ALTURA - 30, LARGURA - ALTURA, font_parametro("calibri", 20), 30
    )
    group_text = pygame.sprite.Group(textField)
    desistir_img = pygame.image.load("images/botao_desistir.jpg")
    botao_desistir = Button(LARGURA - 100, 0, desistir_img, 0.5)
    while not sair:
        event_list = pygame.event.get()
        for evento in event_list:
            if evento.type == pygame.QUIT:
                sair = True
                if tipo == "cliente":
                    cliente.enviar_mensagem("desconectou")
                    cliente.encerrarConexao()
                else:
                    server.enviar_mensagem("desconectou")
                    server.encerrarConexao()
                return True
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if jogo.seu_turno:
                    jogo.avalia_posicao_clicada(pygame.mouse.get_pos())
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    offset += 20
                if evento.key == pygame.K_DOWN:
                    offset -= 20
                if evento.key == pygame.K_RETURN:
                    if tipo == "cliente":
                        cliente.enviar_mensagem(textField.text)
                    else:
                        server.enviar_mensagem(textField.text)
                    textField.text = ""
        if sair:
            break
        display.fill(BRANCO)
        jogo.desenha_tabuleiro()
        criar_chat(textos, offset)
        offset = botoes_chat(offset)
        jogo.desenha_menu()
        textField.update(event_list)
        group_text.draw(display)

        if botao_desistir.draw(display):
            jogo.estado_atual = "Desistiu"
            if tipo == "server":
                server.enviar_mensagem("desistencia")
            else:
                cliente.enviar_mensagem("desistencia")

        jogo.verifica_fim_jogo()
        if jogo.estado_atual != "Jogando":
            encerrar = tela_fim_jogo()
            if encerrar:
                sair = True
                return True

        pygame.display.update()
        clock.tick(60)


def receber_msg(conn):
    while not server.encerrar and not cliente.encerrar:
        try:
            data = conn.recv(1024)
            if not data:
                server.encerrarConexao()
                cliente.encerrarConexao()
                break
            if str(data.decode()).startswith("msg:"):
                mensagem = "Oponente: " + str(data.decode()).split("msg:", 1)[1]
                if len(mensagem) > 27:
                    textos.append(mensagem[:26])
                    textos.append(mensagem[27:])
                else:
                    textos.append(mensagem)
            if str(data.decode()).startswith("jogada:"):
                jogada = str(data.decode())
                jogada = jogada.split("jogada:", 1)[1]
                posicaoInicial = [int(jogada[1]), int(jogada[3])]
                posicaoFinal = [int(jogada[6]), int(jogada[8])]
                jogo.moverPeca(posicaoInicial, posicaoFinal)
            if str(data.decode()) == "desistencia":
                jogo.estado_atual = "Desistencia"
            if str(data.decode()) == "desconectou":
                jogo.estado_atual = "Desconectou"
            if str(data.decode()) == "reiniciar":
                jogo.estado_atual = "Reiniciar"
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            server.encerrar = True
            break


def enviar_msg(conn, msg):
    if (
        msg.startswith("jogada:")
        or msg == "desistencia"
        or msg == "desconectou"
        or msg == "reiniciar"
    ):
        conn.sendall((msg).encode())
    else:
        conn.sendall(("msg:" + msg).encode())
        mensagem = "Você: " + msg
        if len(mensagem) > 27:
            textos.append(mensagem[:26])
            textos.append(mensagem[27:])
        else:
            textos.append(mensagem)


def pegar_porta_livre_tcp():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


def tutorial():
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    tutorial = pygame.image.load("images/tutorial.jpg")
    voltar_img = pygame.image.load("images/botao_voltar.jpg")
    botao_voltar = Button(10, 10, voltar_img, 1)
    encerrar = False
    while not encerrar:
        tela.fill(BRANCO)
        desenhar_background(tela, tutorial)
        if botao_voltar.draw(tela):
            encerrar = True
        event_list = pygame.event.get()
        for evento in event_list:
            if evento.type == pygame.QUIT:
                return True
        pygame.display.update()


def gerar_menu():
    pygame.init()
    telaMenu = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Menu")

    # variaveis
    finish = False

    servidor_img = pygame.image.load("images/botao_servidor.jpg")

    cliente_img = pygame.image.load("images/botao_cliente.jpg")

    sair_img = pygame.image.load("images/botao_sair.jpg")
    tutorial_img = pygame.image.load("images/botao_tutorial.jpg")

    botao_servidor = Button(490, 340, servidor_img, 1)
    botao_cliente = Button(490, 450, cliente_img, 1)
    botao_tutorial = Button(490, 560, tutorial_img, 1)
    botao_sair = Button(490, 670, sair_img, 1)

    run = True
    while run:
        clock.tick(60)
        telaMenu.fill((0, 0, 0))
        desenhar_background(telaMenu, background)

        if not finish:
            if botao_servidor.draw(telaMenu):
                finish = janela_jogo("servidor")
                if finish:
                    break
            if botao_cliente.draw(telaMenu):
                finish = janela_jogo("cliente")
                if finish:
                    break
            if botao_tutorial.draw(telaMenu):
                finish = tutorial()
                if finish:
                    break
            if botao_sair.draw(telaMenu):
                run = False
                break
            draw_text(
                display,
                "Créditos: Mateus Machado Costa",
                font_parametro("arial", 20),
                COR_TABULEIRO,
                0,
                ALTURA - 30,
            )
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()


def janela_jogo(selecao):
    pygame.init()
    pygame.display.set_caption("Jogo Resta Um")
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    voltar_img = pygame.image.load("images/botao_voltar.jpg")
    cliente_img = pygame.image.load("images/botao_cliente.jpg")
    botao_voltar = Button(10, 10, voltar_img, 1)
    botao_entrar = Button(500, 600, cliente_img, 1)

    global server
    global cliente
    server = Server()
    cliente = Cliente()

    def start_server(ip, porta):
        t_server = threading.Thread(target=server.run, args=(ip, porta), daemon=True)
        t_server.start()

    def start_cliente(ip, porta):
        t_cliente = threading.Thread(target=cliente.run, args=(ip, porta), daemon=True)
        t_cliente.start()

    def erro_conexao():
        sair = False
        while not sair:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sair = True
                    return True
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        sair = True
                        cliente.error = None

            display.fill(BRANCO)
            desenhar_background(display, background)
            draw_text(
                display,
                "Erro ao conectar!",
                font,
                PRETO,
                400,
                300,
            )
            draw_text(
                display,
                str(cliente.error),
                font,
                COR_TABULEIRO,
                180,
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

    def entrar_jogo():
        encerrar = False
        ip_input = TextInputBox(250, 480, 400, font, 14)
        port_input = TextInputBox(770, 480, 200, font, 7)
        group_ip = pygame.sprite.Group(ip_input)
        group_port = pygame.sprite.Group(port_input)
        while not encerrar:
            tela.fill(BRANCO)
            desenhar_background(tela, background)
            draw_text(
                tela,
                "Digite o endereço e porta do servidor",
                font,
                PRETO,
                200,
                380,
            )
            draw_text(
                tela,
                "IP:",
                font_parametro("calibri", 30),
                PRETO,
                200,
                500,
            )
            draw_text(
                tela,
                "PORTA:",
                font_parametro("calibri", 30),
                PRETO,
                670,
                500,
            )
            if botao_voltar.draw(tela):
                cliente.encerrarConexao()
                encerrar = True
            if botao_entrar.draw(tela):
                start_cliente(ip_input.text, port_input.text)
            if cliente.conectado == True:
                encerrar = loop_jogo("cliente")
                if encerrar == True:
                    break
            if cliente.error:
                encerrar = erro_conexao()
            event_list = pygame.event.get()
            for evento in event_list:
                if evento.type == pygame.QUIT:
                    encerrar = True
            group_ip.update(event_list)
            group_port.update(event_list)
            group_ip.draw(tela)
            group_port.draw(tela)
            # Atualização da tela
            pygame.display.update()

    def hostear_jogo():
        encerrar = False
        hostname = socket.gethostname()
        porta = pegar_porta_livre_tcp()
        ip = socket.gethostbyname(hostname)
        start_server(ip, porta)
        while not encerrar:
            tela.fill(BRANCO)
            desenhar_background(tela, background)
            draw_text(
                tela,
                "Aguarde o jogador se conectar...",
                font,
                PRETO,
                260,
                380,
            )
            draw_text(
                tela,
                f"Seu IP: {ip} : {porta}",
                font,
                PRETO,
                300,
                450,
            )
            if botao_voltar.draw(tela):
                encerrar = True
                server.encerrarConexao()
            if server.conectado == True:
                encerrar = loop_jogo("server")
                if encerrar == True:
                    break

            # Atualização da tela
            pygame.display.update()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    encerrar = True
                    server.encerrarConexao()

    if selecao == "servidor":
        hostear_jogo()
    if selecao == "cliente":
        entrar_jogo()


gerar_menu()
