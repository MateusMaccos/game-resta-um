# saved as greeting-client.py
import Pyro4
import Pyro4.naming
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

class ServidorNomes:
    def iniciar_servidor_nomes(self):
        t_servidor_nomes = threading.Thread(target=Pyro4.naming.startNSloop, daemon=True)
        t_servidor_nomes.start()

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


    


class Cliente:
    def __init__(self):
        self.id=None
        self.conectado = False
        self.error = False
        self.jogo = None
        self.posicaoInicial=None
        self.posicaoFinal=None
        self.tabuleiro = None

    def run(self, proxy):
        try:
            self.jogo = Pyro4.Proxy("PYRONAME:"+proxy)
            if self.jogo:
                self.tabuleiro = [linha[:] for linha in self.jogo.pegar_tabuleiro()]
                self.conectado=True
                if self.jogo.pegar_qntd_jogadores() == 0:
                    self.jogo.registrar_jogador("Jogador1")
                    self.id="Jogador1"
                else:
                    self.jogo.registrar_jogador("Jogador2")
                    self.id="Jogador2"
        except ConnectionRefusedError:
            print("A conexão foi recusada pelo servidor.")
            self.conectado = False
            self.error = "A conexão foi recusada pelo servidor."
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            self.conectado = False
            self.error = "Não foi possível acessar a sala indicada"

    def estado_atual(self):
        return self.jogo.pegar_estado_atual()
    
    def mudar_estado_atual(self,estado):
        return self.jogo.mudar_estado_atual(estado)

    def seu_turno(self):
        return self.jogo.pegar_turno() == self.id
    
    def enviar_chat(self,msg):
        self.jogo.registrar_msg(self.id,msg)

    def pegar_chat(self):
        return self.jogo.pegar_chat()
    
    def pegar_adversario(self):
        return self.jogo.pegar_adversario(self.id)

    def verifica_fim_jogo(self):
        return self.jogo.verifica_fim_jogo()
    
    def desistiu(self):
        return self.jogo.desistiu(self.id)
    
    def resetar(self):
        return self.jogo.resetar_jogo()
    
    def avalia_posicao_clicada(self, coordenada):
        linha, coluna = linha_clicada(coordenada), coluna_clicada(coordenada)
        if self.posicaoInicial == None:
            if self.tabuleiro[linha][coluna] == 1:
                self.posicaoInicial = [linha, coluna]
        else:
            movimentos = self.jogo.posicoesPossiveis(
                self.posicaoInicial[0], self.posicaoInicial[1]
            )
            if [linha, coluna] in movimentos:
                self.posicaoFinal = [linha, coluna]
                self.jogo.moverPeca(self.posicaoInicial, self.posicaoFinal)
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
                    if [l, c] in self.jogo.posicoesPossiveis(
                        self.posicaoInicial[0], self.posicaoInicial[1]
                    ):
                        pygame.draw.rect(
                            display, VERDE, (x, y, tamanho_quadrado, tamanho_quadrado)
                        )
                x += tamanho_quadrado
            y += tamanho_quadrado

        self.tabuleiro = [linha[:] for linha in self.jogo.pegar_tabuleiro()]
        for l in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[l])):
                x = ALTURA / 7 * c + ALTURA / 14
                y = ALTURA / 7 * l + ALTURA / 14
                if self.tabuleiro[l][c] == 1:
                    pygame.draw.circle(display, BRANCO, (x, y), raio_circulo, 0)

    def desenha_menu(self):
        if self.seu_turno():
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

    def encerrarConexao(self):
        self.jogo.desconectou(self.id)
        # try:
        #     self.jogo.shutdown()
        # except Exception as e:
        #     print(f"Erro ao encerrar conexão: {e}")


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
                if cliente.estado_atual() != "Desconectou":
                    cliente.encerrarConexao()
                return True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    sair = True
                    if cliente.estado_atual() != "Desconectou":
                        cliente.encerrarConexao()
                    return True

        display.fill(BRANCO)
        desenhar_background(display, background)
        if cliente.estado_atual() == 'Esperando':
            titulo = "Esperando jogador"
            jogadores = cliente.jogo.pegar_qntd_jogadores()
            margem=400
            draw_text(
                display,
                f"{jogadores}/2",
                font,
                PRETO,
                580,
                400,
            )
        else:
            titulo = "Fim de jogo!"
            margem=480
        draw_text(
            display,
            titulo,
            font,
            PRETO,
            margem,
            300,
        )
        if cliente.estado_atual() == "Jogando":
            return False
        if cliente.estado_atual() in ["Empate", "Fim"]:
            if botao_reiniciar.draw(display):
                cliente.resetar()
        if cliente.estado_atual() == "Empate":
            draw_text(
                display,
                "Empate",
                font_maior,
                COR_TABULEIRO,
                480,
                400,
            )
        elif cliente.estado_atual() == "Fim":
            if not cliente.seu_turno():
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
        elif cliente.estado_atual()=="Desistencia":
            if cliente.seu_turno():
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
        elif cliente.estado_atual() == "Desconectou":
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
    return False


def criar_chat(textos, offset):
    PADDING = ALTURA - 115
    MARGIN = 50
    pygame.draw.rect(display, CINZA, (ALTURA, 120, LARGURA - ALTURA, ALTURA - 120))
    cor = None
    oponente = cliente.pegar_adversario()
    for texto in reversed(textos):
        posicao = ALTURA
        if texto.__contains__(cliente.id):
            text_surface = font_parametro("calibri", 30).render(
                texto, True, CINZA_CLARO
            )
        elif texto.__contains__(oponente):
            text_surface = font_parametro("calibri", 30).render(texto, True, PRETO)
        else:
            if textos[textos.index(texto) - 1].__contains__(cliente.id):
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


def loop_jogo():
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
                cliente.encerrarConexao()
                return True
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if cliente.seu_turno():
                    cliente.avalia_posicao_clicada(pygame.mouse.get_pos())
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    offset += 20
                if evento.key == pygame.K_DOWN:
                    offset -= 20
                if evento.key == pygame.K_RETURN:
                    cliente.enviar_chat(textField.text)
                    textField.text = ""
        if sair:
            break
        display.fill(BRANCO)
        cliente.desenha_tabuleiro()
        criar_chat(cliente.pegar_chat(), offset)
        offset = botoes_chat(offset)
        cliente.desenha_menu()
        textField.update(event_list)
        group_text.draw(display)

        if botao_desistir.draw(display):
            cliente.desistiu()
        cliente.verifica_fim_jogo()
        if cliente.estado_atual() != "Jogando":
            encerrar = tela_fim_jogo()
            if encerrar:
                sair = True
                return True

        pygame.display.update()
        clock.tick(60)

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
                finish = janela_jogo('servidor')
                if finish:
                    break
            if botao_cliente.draw(telaMenu):
                finish = janela_jogo('cliente')
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

    global cliente
    cliente = Cliente()

    def start_cliente(proxy):
        t_cliente = threading.Thread(target=cliente.run, args=(proxy,), daemon=True)
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
        proxy_input = TextInputBox(400, 480, 400, font, 14)
        group_proxy = pygame.sprite.Group(proxy_input)
        while not encerrar:
            tela.fill(BRANCO)
            desenhar_background(tela, background)
            draw_text(
                tela,
                "Digite o nome cadastrado do servidor",
                font,
                PRETO,
                200,
                380,
            )
            if botao_voltar.draw(tela):
                encerrar = True
            if botao_entrar.draw(tela):
                start_cliente(proxy_input.text)
            if cliente.conectado == True:
                encerrar = loop_jogo()
                if encerrar == True:
                    break
            if cliente.error:
                encerrar = erro_conexao()
            event_list = pygame.event.get()
            for evento in event_list:
                if evento.type == pygame.QUIT:
                    encerrar = True
            group_proxy.update(event_list)
            group_proxy.draw(tela)
            # Atualização da tela
            pygame.display.update()
    
    def servidor_de_nomes():
        encerrar = False
        SN = ServidorNomes()
        SN.iniciar_servidor_nomes()
        while not encerrar:
            tela.fill(BRANCO)
            desenhar_background(tela, background)
            draw_text(
                tela,
                "Servidor de nomes iniciado",
                font,
                PRETO,
                260,
                380,
            )
            if botao_voltar.draw(tela):
                encerrar = True

            # Atualização da tela
            pygame.display.update()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    encerrar = True

    if selecao == "servidor":
        servidor_de_nomes()
    if selecao == "cliente":
        entrar_jogo()

gerar_menu()
