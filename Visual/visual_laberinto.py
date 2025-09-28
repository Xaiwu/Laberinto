from Logica.laberinto import Laberinto
from Visual import visual_controller as CONFIG #type:ignore
import pygame #type:ignore

class LaberintoVisual:
    def __init__(self,laberinto,tam_bloque):
        self.laberinto = laberinto
        self.tam_bloque = tam_bloque

    def run(self,pantalla):
        self.laberinto.mover_paredes()
        self.pantalla = pantalla
        self.pantalla.fill(CONFIG.BLANCO)
        self.dibujar_grid()

        pygame.time.Clock().tick(30)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

    # Dibujar el laberinto
    def dibujar_grid(self):
        for i in range(self.laberinto.n):
            for j in range(self.laberinto.n):
                x, y = j*self.tam_bloque, i*self.tam_bloque
                if self.laberinto.grid[i][j] == Laberinto.PARED:
                    pygame.draw.rect(self.pantalla,CONFIG.NEGRO, (x, y,self.tam_bloque,self.tam_bloque))
                if self.laberinto.grid[i][j] == Laberinto.SALIDA:
                    pygame.draw.rect(self.pantalla,CONFIG.VERDE, (x, y,self.tam_bloque,self.tam_bloque))
                if self.laberinto.grid[i][j] == Laberinto.SALIDA_REAL:
                    pygame.draw.rect(self.pantalla,CONFIG.VERDE, (x, y,self.tam_bloque,self.tam_bloque))
                pygame.draw.rect(self.pantalla, CONFIG.GRIS, (x, y, self.tam_bloque,self.tam_bloque),1)
