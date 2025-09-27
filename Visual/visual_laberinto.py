from Logica.laberinto import Laberinto
from Visual import visual_controller as CONFIG #type:ignore
import pygame #type:ignore

class LaberintoVisual:
    def __init__(self,laberinto,tam_bloque):
        self.laberinto = laberinto
        self.tam_bloque = tam_bloque

    def run(self,pantalla):
        self.pantalla = pantalla
        self.pantalla.fill(CONFIG.BLANCO)
        self.dibujar_grid()

    def event(self, event):
        if event.key == pygame.K_SPACE:
            self.laberinto.mover_paredes()

    # Dibujar el laberinto
    def dibujar_grid(self):
        for i in range(self.laberinto.n):
            for j in range(self.laberinto.n):
                x, y = j*self.tam_bloque, i*self.tam_bloque
                if self.laberinto.grid[i][j] == Laberinto.PARED:
                    pygame.draw.rect(self.pantalla,CONFIG.NEGRO, (x, y,self.tam_bloque,self.tam_bloque))
                if self.laberinto.grid[i][j] == Laberinto.SALIDA:
                    pygame.draw.rect(self.pantalla,CONFIG.ROJO, (x, y,self.tam_bloque,self.tam_bloque))
                pygame.draw.rect(self.pantalla, CONFIG.GRIS, (x, y, self.tam_bloque,self.tam_bloque),1)
