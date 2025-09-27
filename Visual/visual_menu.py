from Visual import visual_controller as CONFIG #type:ignore
import pygame

class Menu:
    def __init__(self):
        self.buttons = []
        pass

    def run(self,pantalla):
        self.__pantalla = pantalla
        self.__pantalla.fill(CONFIG.NEGRO)
        self.button_start = button(pantalla,300,300,300,100)
        self.buttons = [self.button_start]

    def event(self, event:pygame.event):
        for b in self.buttons:
            b.event(event)


class button:
    def __init__(self,pantalla,x_pos,y_pos,w_size,h_size):
        self.pos = (x_pos-w_size/2,y_pos-h_size/2)
        self.size = (w_size,h_size)
        self.button_rect = pygame.Rect(self.pos,self.size)
        self.pantalla = pantalla
        self.draw()
        pass

    def event(self, event:pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                print("¡Botón presionado!")

    def draw(self):
        pygame.draw.rect(self.pantalla,CONFIG.BLANCO, self.button_rect)
        pass

