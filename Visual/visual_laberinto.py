import copy

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
        print(self.laberinto.salida_real.posicion)

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
        pasos, fit = genetico.algoritmo_genetico(self.agente.lab)

        pos_fila = []
        lab_fila = []
        np = (0,0)
        while pasos.__len__() > 0: # type:ignore
            var = pasos.pop(0)
            self.pantalla.fill(CONFIG.BLANCO)
            if var == 'DOWN':
                np = (np[0],np[1]+1)
            if var == 'UP':
                np = (np[0],np[1]-1)
            if var == 'RIGHT':
                np = (np[0] + 1,np[1])
            if var == 'LEFT':
                np = (np[0] - 1,np[1])

            if self.agente.lab.es_pared(np) or not self.agente.lab.en_rango(np):
                np = (0,0)
                pasos, fit = genetico.algoritmo_genetico(self.agente.lab)
                pos_fila = []
                lab_fila = []
            else:
                pos_fila.append(np)
                lab_fila.append(copy.deepcopy(self.agente.lab.grid))
            self.agente.lab.mover_paredes(np)

        while pos_fila.__len__() > 0:
            self.pantalla.fill(CONFIG.BLANCO)
            np = pos_fila.pop(0)
            self.agente.lab.grid = lab_fila.pop(0)
            self.agente.posicion = np

            pygame.time.wait(100)

            self.dibujar_grid()
            self.dibujar_agente()
            pygame.display.flip()

        pygame.time.wait(2000)


    # Dibujar el laberinto
    def dibujar_grid(self):
        for i in range(self.laberinto.n):
            for j in range(self.laberinto.n):
                x, y = i*self.tam_bloque, j*self.tam_bloque
                if self.agente.lab.grid[i][j] == Laberinto.PARED:
                    pygame.draw.rect(self.pantalla,CONFIG.NEGRO, (x, y,self.tam_bloque,self.tam_bloque))
                if self.agente.lab.grid[i][j] == Laberinto.SALIDA:
                    pygame.draw.rect(self.pantalla,CONFIG.VERDE, (x, y,self.tam_bloque,self.tam_bloque))
                if self.agente.lab.grid[i][j] == Laberinto.SALIDA_REAL:
                    pygame.draw.rect(self.pantalla,CONFIG.VERDE, (x, y,self.tam_bloque,self.tam_bloque))
                pygame.draw.rect(self.pantalla, CONFIG.GRIS, (x, y, self.tam_bloque,self.tam_bloque),1)

    def dibujar_agente(self):
        x, y = self.agente.posicion[0]*self.tam_bloque, self.agente.posicion[1]*self.tam_bloque
        pygame.draw.rect(self.pantalla,CONFIG.AZUL, (x, y,self.tam_bloque,self.tam_bloque))
