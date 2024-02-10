# Configurações iniciais
import pygame
import button
import textInput
import socket
import socketServer
import socketCliente
import threading


def pegar_porta_livre_tcp():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


def draw_text(tela, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    tela.blit(img, (x, y))


def desenhar_background(tela, image):
    size = pygame.transform.scale(image, (1200, 800))
    tela.blit(image, (0, 0))


def gerar_menu():
    pygame.init()
    larguraMenu, alturaMenu = 1200, 800
    telaMenu = pygame.display.set_mode((larguraMenu, alturaMenu))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Menu")

    # variaveis
    failed = False

    font = pygame.font.SysFont("arialblack", 40)

    textColor = (255, 255, 255)

    background = pygame.image.load("images/menu.jpg")

    servidor_img = pygame.image.load("images/botao_servidor.jpg")

    cliente_img = pygame.image.load("images/botao_cliente.jpg")

    sair_img = pygame.image.load("images/botao_sair.jpg")

    botao_servidor = button.Button(490, 360, servidor_img, 1)
    botao_cliente = button.Button(490, 470, cliente_img, 1)
    botao_sair = button.Button(490, 580, sair_img, 1)

    run = True
    while run:
        clock.tick(60)
        telaMenu.fill((0, 0, 0))
        desenhar_background(telaMenu, background)

        if failed == False:
            if botao_servidor.draw(telaMenu):
                janela_jogo("servidor")
            if botao_cliente.draw(telaMenu):
                janela_jogo("cliente")
            if botao_sair.draw(telaMenu):
                run = False
        elif failed == "sair":
            run = False
        else:
            draw_text(
                "Você perdeu, aperte espaço para ir pro menu!",
                font,
                textColor,
                100,
                380,
            )
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    failed = False
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


def janela_jogo(selecao):
    pygame.init()
    pygame.display.set_caption("Jogo Resta Um")
    largura, altura = 1200, 800
    tela = pygame.display.set_mode((largura, altura))
    font = pygame.font.SysFont("arialblack", 40)
    background = pygame.image.load("images/menu.jpg")
    voltar_img = pygame.image.load("images/botao_voltar.jpg")
    cliente_img = pygame.image.load("images/botao_cliente.jpg")
    botao_voltar = button.Button(10, 10, voltar_img, 1)
    botao_entrar = button.Button(500, 600, cliente_img, 1)

    # Cores - RGB
    preta = (0, 0, 0)
    branca = (255, 255, 255)

    def entrar_jogo():
        encerrar = False
        ip_input = textInput.TextInputBox(400, 500, 400, font)
        port_input = textInput.TextInputBox(900, 500, 100, font)
        group_ip = pygame.sprite.Group(ip_input)
        group_port = pygame.sprite.Group(port_input)
        while not encerrar:
            tela.fill(branca)
            desenhar_background(tela, background)
            draw_text(
                tela,
                "Digite o endereço e porta do servidor",
                font,
                preta,
                200,
                380,
            )
            if botao_voltar.draw(tela):
                encerrar = True
            if botao_entrar.draw(tela):
                socketCliente.cliente(ip_input.text, port_input)

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
        conectou = False
        encerrar = False
        hostname = socket.gethostname()
        porta = pegar_porta_livre_tcp()
        ip = socket.gethostbyname(hostname)
        while not conectou and not encerrar:
            tela.fill(branca)
            desenhar_background(tela, background)
            draw_text(
                tela,
                "Aguarde o jogador se conectar...",
                font,
                preta,
                260,
                380,
            )
            draw_text(
                tela,
                f"Seu IP: {ip} : {porta}",
                font,
                preta,
                300,
                450,
            )
            if botao_voltar.draw(tela):
                encerrar = True

            # Atualização da tela
            pygame.display.update()
            socketServer.servidor(ip, porta)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    conectou = True

    if selecao == "servidor":
        hostear_jogo()
    if selecao == "cliente":
        entrar_jogo()


gerar_menu()
