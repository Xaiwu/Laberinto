import copy
import random

MOVIMIENTOS = ["UP", "DOWN", "LEFT", "RIGHT"]

class Agente:
    def __init__(self, lab, inicio=(0, 0)):
        self.lab = lab
        self.x, self.y = inicio

    def mover(self, direccion):
        nx, ny = self.x, self.y
        # Calcular posición destino
        if direccion == "LEFT": nx, ny = self.x - 1, self.y
        elif direccion == "RIGHT": nx, ny = self.x + 1, self.y
        elif direccion == "UP": nx, ny = self.x, self.y - 1
        elif direccion == "DOWN": nx, ny = self.x, self.y + 1

        # Verificar si puede moverse
        if 0 <= nx < self.lab.n and 0 <= ny < self.lab.n:
            if not self.lab.es_pared((nx, ny)):
                self.x, self.y = nx, ny
                return True  # movimiento exitoso
        return False  # bloqueado por pared o borde

    def posicion_actual(self):
        return (self.x,self.y)

# Generar población inicial
def población_inicial(poblacion = 50, movimientos = 20):
    población = []
    for i in range(poblacion):
        #creamos una variación de caminos aleatorios
        cromosoma = [random.choice(MOVIMIENTOS) for i in range(movimientos)]
        población.append(cromosoma)
    return población

# Función de evaluación, mide desempeño del agente
def fitness(cromosoma, lab, inicio=(0, 0), devolver_estados=False):
    agente = Agente(lab, inicio)
    num_movimiento = 1

    for mov in cromosoma:
        # Verificar si el agente quedó atrapado
        if lab.es_pared(agente.posicion_actual()):
            return (0, []) if devolver_estados else 0

        # Intentar mover
        exito = agente.mover(mov)
        if exito == False:
            return (0, []) if devolver_estados else 0

        # Verificar si llegó a la salida real
        if lab.es_salida_real(agente.posicion_actual()):
            return (1000 + (len(cromosoma) - num_movimiento)) if devolver_estados else 1000 + (len(cromosoma) - num_movimiento)

        num_movimiento += 1

    # Calcular distancia a la salida real
    x, y = agente.posicion_actual()
    salida_x, salida_y = lab.salida_real.posicion
    distancia = abs(x - salida_x) + abs(y - salida_y)

    resultado = 1 / (1 + distancia)

    # Retornar fitness y estados (si se pidió)
    return (resultado) if devolver_estados else resultado


def seleccion(poblacion, lab, inicio, k=5):
    # Seleccionamos k candidatos al azar
    candidatos = random.sample(poblacion, k)

    # Evaluamos el fitness de cada candidato
    mejor = candidatos[0]
    mejor_fitness = fitness(mejor, lab, inicio)

    for individuo in candidatos[1:]:
        fit = fitness(individuo, lab, inicio)
        if fit > mejor_fitness:
            mejor = individuo
            mejor_fitness = fit
    # Retornamos el mejor entre los k
    return mejor

# Reproducción por punto de corte
def reproducir(padre1, padre2):
    c = random.randint(1, len(padre1) - 1)
    return padre1[:c] + padre2[c:]

# Mutación aleatoria
def mutacion(cromosoma, prob=0.1):
    for i in range(len(cromosoma)):
        if random.random() < prob:
            cromosoma[i] = random.choice(MOVIMIENTOS)
    return cromosoma

# Algoritmo genético principal
def algoritmo_genetico(lab, inicio=(0, 0), generaciones=120, poblacion=50, movimientos=20):
    poblacion_actual = población_inicial(poblacion, movimientos)
    mejor, mejor_fit = None, float("-inf")

    for gen in range(generaciones):
        nueva_poblacion = []

        # Elitismo
        if mejor:
            nueva_poblacion.append(copy.deepcopy(mejor))
        # Reproducción y mutación
        for _ in range(poblacion - 1):
            padre1 = seleccion(poblacion_actual, lab, inicio)
            padre2 = seleccion(poblacion_actual, lab, inicio)
            hijo = reproducir(padre1, padre2)
            hijo = mutacion(hijo, prob=0.1)
            nueva_poblacion.append(hijo)

        # Evaluar nueva generación
        poblacion_actual = nueva_poblacion
        for cromosoma in poblacion_actual:
            f = fitness(cromosoma, lab, inicio)
            if f > mejor_fit:
                mejor_fit, mejor = f, cromosoma

        print(f"Generación {gen + 1}: mejor fitness = {round(mejor_fit, 3)}")
    # recortamos el cromosoma hasta donde llegó a la salida
    agente = Agente(lab, inicio)
    pasos_validos = 0
    for mov in mejor:
        agente.mover(mov)
        pasos_validos += 1
        if lab.es_salida_real(agente.posicion_actual()):
            break  # si llegó, salir del bucle
    mejor = mejor[:pasos_validos]

    # retornamos también el historial junto al mejor y su fitness
    return mejor, mejor_fit
