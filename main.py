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
    visual_estado_laberinto = LaberintoVisual(l,tam_celda)
    v_controller.setEstado(visual_estado_laberinto)
    pass

v_controller = VisualController(ANCHO,ALTO)
b_start = visual_estado_menu.create_button(ANCHO/2,ALTO-100,300,100,change_laberinto)
b_start.set_title("Start")

sel_1 = visual_estado_menu.create_selector(ANCHO/2,ALTO/2-100,50,["10","20","25","50","100"])
sel_1.set_title("Tamaño del laberinto:")

sel_2 = visual_estado_menu.create_selector(ANCHO/2,ALTO/2,50,["10","20","25","50","100"])
sel_2.set_title("Cantidad de paredes:")

v_controller.setEstado(visual_estado_menu)
v_controller.start()

