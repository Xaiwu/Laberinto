from re import S

from Logica.laberinto import Laberinto
from Visual import visual_controller as CONFIG #type:ignore
import pygame

from algoritmos import genetico
from algoritmos.A_star_repetido import ARepetido


class LaberintoVisual:
    def __init__(self,laberinto,tam_bloque,modo):
        self.laberinto = laberinto
        self.tam_bloque = tam_bloque
        self.first_called = False
        self.modo = modo

        self.agente = ARepetido(
                inicio=(0,0),
                salidas=self.laberinto.salidas,
                laberinto=self.laberinto,
                prob_mover_paredes=0.2,
                debug=False,
                modo='exploracion',   # 'exploracion' o 'normal'
                vision=2,
            )

    def run(self,pantalla):
        self.pantalla = pantalla
        self.pantalla.fill(CONFIG.BLANCO)
        self.first_call()
        self.dibujar_grid()
        self.dibujar_agente()

        pygame.display.flip()

        #pygame.time.Clock().tick(30)

    def first_call(self):
        if self.first_called:
            return

        self.first_called = True

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.llamar_alg()

    def llamar_alg(self):
        if self.modo == "A*":
            b,r = self.agente.paso() # Algoritmo A*

            if r == 'W':
                print("GANASTE!")
        else:
            self.alg_genetico()

    def alg_genetico(self):
        pasos, fit, h = genetico.algoritmo_genetico(self.agente.lab)
        print(pasos)

        h_int = 0
        for var in pasos: # type:ignore
            h_int += 1
            self.pantalla.fill(CONFIG.BLANCO)
            if var == 'LEFT':
                self.agente.posicion = (self.agente.posicion[0],self.agente.posicion[1]-1)
            if var == 'RIGHT':
                self.agente.posicion = (self.agente.posicion[0],self.agente.posicion[1]+1)
            if var == 'DOWN':
                self.agente.posicion = (self.agente.posicion[0] + 1,self.agente.posicion[1])
            if var == 'UP':
                self.agente.posicion = (self.agente.posicion[0] - 1,self.agente.posicion[1])

            pygame.time.wait(300)
            if h_int < h.__len__():
                self.agente.lab.grid = h[h_int]

            self.dibujar_grid()
            self.dibujar_agente()
            pygame.display.flip()

        pygame.time.wait(2000)
        pygame.quit()


    # Dibujar el laberinto
    def dibujar_grid(self):
        for i in range(self.laberinto.n):
            for j in range(self.laberinto.n):
                x, y = j*self.tam_bloque, i*self.tam_bloque
                if self.agente.lab.grid[i][j] == Laberinto.PARED:
                    pygame.draw.rect(self.pantalla,CONFIG.NEGRO, (x, y,self.tam_bloque,self.tam_bloque))
                if self.agente.lab.grid[i][j] == Laberinto.SALIDA:
                    pygame.draw.rect(self.pantalla,CONFIG.VERDE, (x, y,self.tam_bloque,self.tam_bloque))
                if self.agente.lab.grid[i][j] == Laberinto.SALIDA_REAL:
                    pygame.draw.rect(self.pantalla,CONFIG.VERDE, (x, y,self.tam_bloque,self.tam_bloque))
                pygame.draw.rect(self.pantalla, CONFIG.GRIS, (x, y, self.tam_bloque,self.tam_bloque),1)

    def dibujar_agente(self):
        x, y = self.agente.posicion[1]*self.tam_bloque, self.agente.posicion[0]*self.tam_bloque
        pygame.draw.rect(self.pantalla,CONFIG.AZUL, (x, y,self.tam_bloque,self.tam_bloque))
