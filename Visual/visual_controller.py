import pygame #type:ignore

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
GRIS = (200, 200, 200)

class VisualController:

    def __init__(self,window_width,window_height):
        self.__estado = None
        self.height = window_height
        self.width = window_width

    # Start window
    def start(self):
        self.__running = True

        pygame.init()
        self.__pantalla = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Laberinto")
        self.__pantalla.fill(BLANCO)

        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                self.__estado.event(event) #type:ignore

            self.__estado.run(self.__pantalla) #type:ignore
            pygame.display.flip()

        pygame.quit()

    def setEstado(self,estado):
        self.__estado = estado
