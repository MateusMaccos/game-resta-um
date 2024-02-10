import pygame


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
