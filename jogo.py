# Configurações iniciais
import pygame
import random
import button


def gerar_menu():
    pygame.init()
    larguraMenu, alturaMenu = 1200, 800
    telaMenu = pygame.display.set_mode((larguraMenu, alturaMenu))
    pygame.display.set_caption("Menu")

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        telaMenu.blit(img, (x, y))

    def desenhar_background(image):
        size = pygame.transform.scale(image, (1200, 800))
        telaMenu.blit(image, (0, 0))

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
        telaMenu.fill((0, 0, 0))
        desenhar_background(background)

        if failed == False:
            if botao_servidor.draw(telaMenu):
                run = False
            if botao_cliente.draw(telaMenu):
                run = False
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

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    failed = False
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


gerar_menu()
