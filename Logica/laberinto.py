import random
from Logica.pared import Pared
from Logica.salida import Salida


class Laberinto:
    VACIO = 0
    PARED = 1
    SALIDA = 2
    SALIDA_REAL = 3

    def __init__(self, n, num_paredes, num_salidas):
        self.n = n
        self.grid = [[self.VACIO for _ in range(n)] for _ in range(n)]
        self.paredes = []
        self.salidas = []
        self.salida_real = None

        # Colocar paredes aleatorias
        while len(self.paredes) < num_paredes:
            x, y = random.randint(0, n-1), random.randint(0, n-1)
            if self.grid[x][y] == self.VACIO:
                self.grid[x][y] = self.PARED
                self.paredes.append(Pared((x, y)))

        # Colocar salidas aleatorias
        while len(self.salidas) < num_salidas:
            x, y = random.randint(0, n-1), random.randint(0, n-1)
            if self.grid[x][y] == self.VACIO:
                self.grid[x][y] = self.SALIDA
                self.salidas.append(Salida((x, y)))

        # Elegir una salida real
        self.salida_real = random.choice(self.salidas)
        x, y = self.salida_real.posicion
        self.grid[x][y] = self.SALIDA_REAL
        self.salida_real.es_real = True

    def es_pared(self, pos):
        return self.grid[pos[0]][pos[1]] == self.PARED

    def es_salida(self, pos):
        return self.grid[pos[0]][pos[1]] in (self.SALIDA, self.SALIDA_REAL)

    def es_salida_real(self, pos):
        return self.grid[pos[0]][pos[1]] == self.SALIDA_REAL

    def en_rango(self, pos):
        x, y = pos
        return 0 <= x < self.n and 0 <= y < self.n

    def mover_paredes(self, pos_agente, prob=0.2):
        """Con probabilidad 'prob', mueve cada pared a una casilla vacía"""
        nuevas_paredes = []
        for pared in self.paredes:
            if random.random() < prob:
                vacias = [(nx, ny) for nx, ny in self.vecinos(pared.posicion)
                        if self.grid[nx][ny] == self.VACIO and (nx, ny) != pos_agente]
                if vacias:
                    self.grid[pared.posicion[0]][pared.posicion[1]] = self.VACIO
                    pared.mover([random.choice(vacias)]) 
                    self.grid[pared.posicion[0]][pared.posicion[1]] = self.PARED
            nuevas_paredes.append(pared)
        self.paredes = nuevas_paredes

    def vecinos(self, pos):
        x, y = pos
        moves = [(-1,0),(1,0),(0,-1),(0,1)]
        vecinos = []
        for dx, dy in moves:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.n and 0 <= ny < self.n:
                vecinos.append((nx, ny))
        return vecinos

    def mostrar(self, pos_agente=None):
        simbolos = {self.VACIO: ' ', self.PARED: '#', self.SALIDA: 'S', self.SALIDA_REAL: 'R'}
        for i, fila in enumerate(self.grid):
            fila_str = ""
            for j, celda in enumerate(fila):
                if pos_agente is not None and (i, j) == pos_agente:
                    fila_str += 'A'
                else:
                    fila_str += simbolos[celda]
            print(fila_str)
