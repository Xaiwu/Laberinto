import pygame # type:ignore
from collections import deque

# Configuración
ANCHO, ALTO = 600, 600
FILAS, COLUMNAS = 20, 20
TAM_CELDA = ANCHO // COLUMNAS

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
GRIS = (200, 200, 200)

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laberinto con BFS")

# Laberinto simple (0 = camino, 1 = pared)
laberinto = [[0]*COLUMNAS for _ in range(FILAS)]
# Agregar algunas paredes de ejemplo
for i in range(5, 15):
    laberinto[10][i] = 1

inicio = (0, 0)
meta = (19, 19)

# Algoritmo BFS
def bfs(inicio, meta):
    cola = deque([inicio])
    visitado = {inicio: None}

    while cola:
        x, y = cola.popleft()

        if (x, y) == meta:
            break

        # Movimientos: arriba, abajo, izquierda, derecha
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < FILAS and 0 <= ny < COLUMNAS:
                if laberinto[nx][ny] == 0 and (nx, ny) not in visitado:
                    cola.append((nx, ny))
                    visitado[(nx, ny)] = (x, y)
                    # Dibujar celda explorada
                    pygame.draw.rect(pantalla, AZUL, (ny*TAM_CELDA, nx*TAM_CELDA, TAM_CELDA, TAM_CELDA))
                    pygame.display.flip()
                    pygame.time.delay(30)

    # Reconstruir camino
    camino = []
    nodo = meta
    while nodo is not None:
        camino.append(nodo)
        nodo = visitado.get(nodo, None)
    camino.reverse()
    return camino

