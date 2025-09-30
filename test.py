import time
import random
import copy
import pandas as pd

from Logica.laberinto import Laberinto
from algoritmos.A_star_repetido import ARepetido
from algoritmos.genetico import algoritmo_genetico_dinamico

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

def run_genetico(lab, prob_move,mov):
    agente = ARepetido(
        inicio=(0, 0),
        salidas=lab.salidas,
        laberinto=lab,
        prob_mover_paredes=prob_move,
        debug=False,
    )
    t0 = time.time()
    pos_fila,_ = algoritmo_genetico_dinamico(agente.lab,prob_move,movimientos=mov)
    pasos = pos_fila.__len__()

    t1 = time.time()
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
    archivo_detalle = "resultados_experimentos_detalle.csv",
    separador = ";"
):
    seed = random.random()
    random.seed(seed)
    resultados = []

    for tamaño in tamaños:
        for prob in prob_movimientos:
            for r in range(repeticiones):
                lab_base, num_pared = crear_laberinto(tamaño, 0.2, num_salidas)
                seed += 1
                random.seed(seed)
                for mode in range(2):
                    lab_aux = copy.deepcopy(lab_base)
                    if mode == 0:
                        alg = "A*_Repetido"
                        tiempo, pasos = run_a_repetido(
                            lab_aux,
                            prob_move=prob,
                            modo='exploracion',
                            vision=2
                        )
                    else:
                        alg = "Genético"
                        tiempo, pasos = run_genetico(
                            lab_aux,
                            prob_move=prob,
                            mov = int(5*tamaño)
                        )

                    registro = {
                        "algoritmo": alg,
                        "tamaño": tamaño,
                        "num_pared": num_pared,
                        "prob_movimiento": prob,
                        "longitud_camino": pasos,
                        "tiempo_segundos": tiempo,
                    }
                    resultados.append(registro)
                    print(f"tam: {tamaño}, pasos: {pasos}, prob: {prob}, repetición: {r} de {alg} listo!")

    df = pd.DataFrame(resultados)
    print(df.head())

    df.to_csv(archivo_detalle, index=False, sep=separador)
    print(f"\nArchivo detalle guardado: {archivo_detalle}")

    return df

if __name__ == "__main__":
    ejecutar_experimentos()
