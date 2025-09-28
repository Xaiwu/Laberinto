import random
from Logica.laberinto import Laberinto
from Visual.visual_controller import VisualController
from Visual.visual_laberinto import LaberintoVisual
from Visual.visual_menu import Menu

# Configuración
ANCHO, ALTO = 600, 600

visual_estado_menu = Menu()

def change_laberinto():
    tam = int(sel_1.actual_value)
    paredes = int(sel_2.actual_value)
    tam_celda = ANCHO // tam 
    l = Laberinto(tam,paredes,10)
    visual_estado_laberinto = LaberintoVisual(l,tam_celda,sel_3.actual_value)
    v_controller.setEstado(visual_estado_laberinto)
    pass

v_controller = VisualController(ANCHO,ALTO)
b_start = visual_estado_menu.create_button(ANCHO/2,ALTO-100,300,100,change_laberinto)
b_start.set_title("Start")

sel_1 = visual_estado_menu.create_selector(ANCHO/2,100,50,["10","20","25","50","100"])
sel_1.set_title("Tamaño del laberinto:")

sel_2 = visual_estado_menu.create_selector(ANCHO/2,200,50,["10","20","25","50","100"])
sel_2.set_title("Cantidad de paredes:")

sel_3 = visual_estado_menu.create_selector(ANCHO/2,300,50,["Genético","A*"])
sel_3.set_title("Algorítmo:")

v_controller.setEstado(visual_estado_menu)
v_controller.start()

"""
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
"""
