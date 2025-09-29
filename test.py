import time
import random
import copy
import pandas as pd

from Logica.laberinto import Laberinto
from algoritmos.A_star_repetido import ARepetido

def run_a_repetido(lab, prob_move, modo='exploracion', vision=2):
    agente = ARepetido(
        inicio=(0, 0),
        salidas=lab.salidas,
        laberinto=lab,
        prob_mover_paredes=prob_move,
        debug=False,
        modo=modo,
        vision=vision
    )
    t0 = time.time()
    agente.run(interactivo=False)
    t1 = time.time()
    pasos = agente.pasos
    return t1 - t0, pasos 

def crear_laberinto(tamaño, pared_densidad, num_salidas):
    n = tamaño * tamaño
    num_pared = int(n * pared_densidad)
    lab = Laberinto(tamaño, num_pared, num_salidas)
    return lab, num_pared

def ejecutar_experimentos(
    tamaños = [10, 20, 30],
    prob_movimientos = [0.1, 0.2, 0.4],
    num_salidas = 6,
    repeticiones = 5,
    seed = 42,
    archivo_detalle = "resultados_experimentos_detalle.csv",
    separador = ";"
):
    random.seed(seed)
    resultados = []

    for tamaño in tamaños:
        for prob in prob_movimientos:
            for rep in range(repeticiones):
                lab_base, num_pared = crear_laberinto(tamaño, 0.2, num_salidas)
                lab_for_astar = copy.deepcopy(lab_base)
                tiempo, pasos = run_a_repetido(
                    lab_for_astar,
                    prob_move=prob,
                    modo='exploracion',
                    vision=2
                )
                registro = {
                    "algoritmo": "A*_Repetido",
                    "tamaño": tamaño,
                    "num_pared": num_pared,
                    "prob_movimiento": prob,
                    "longitud_camino": pasos,
                    "tiempo_segundos": tiempo,
                }
                resultados.append(registro)

    df = pd.DataFrame(resultados)
    print(df.head())

    df.to_csv(archivo_detalle, index=False, sep=separador)
    print(f"\nArchivo detalle guardado: {archivo_detalle}")

    return df

if __name__ == "__main__":
    ejecutar_experimentos()