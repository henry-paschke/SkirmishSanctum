import pygame as pg

class Button():
    def __init__(self, text, rect, function):
        self.text = text
        self.rect = rect
        self.function = function

    def draw(self, screen):
        pg.draw.rect(screen, (255, 255, 255), self.rect)
        font = pg.font.Font(None, 30)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.function()


class Toggle_button(Button):
    def __init__(self, text, rect) -> None:
        self.toggled = False
        super().__init__(text, rect, lambda: self.toggle())

    def toggle(self):
        self.toggled = not self.toggled