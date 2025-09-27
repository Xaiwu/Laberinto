from Logica.laberinto import Laberinto
from algoritmos.A_star_repetido import ARepetido

if __name__ == "__main__":
    n = 10
    lab = Laberinto(n, num_paredes=2*n, num_salidas=3)

    salidas = [s.posicion for s in lab.salidas]
    print("Salidas (ocultas al agente como reales/falsas):", salidas)

    agenteR = ARepetido(
        inicio=(0,0),
        salidas=salidas,
        laberinto=lab,
        prob_mover_paredes=0.2,
        debug=False,
        modo='exploracion',   # 'exploracion' o 'normal'
        vision=2,
    )
    agenteR.run(interactivo=True)