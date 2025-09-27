from Logica.laberinto import Laberinto
from Visual.visual_controller import VisualController
from Visual.visual_laberinto import LaberintoVisual
from Visual.visual_menu import Menu

# Configuración
ANCHO, ALTO = 600, 600
TAM = 10 
TAM_CELDA = ANCHO // TAM 

l = Laberinto(TAM,TAM,10)
visual_estado_laberinto = LaberintoVisual(l,TAM_CELDA)

visual_estado_menu = Menu()
def change_laberinto():
    v_controller.setEstado(visual_estado_laberinto)
    pass

v_controller = VisualController(ANCHO,ALTO)
b_start = visual_estado_menu.create_button(ANCHO/2,ALTO/2,300,100,change_laberinto)
b_start.set_title("Start")

sel_1 = visual_estado_menu.create_selector(ANCHO/2,ALTO/2-100,50,["hola","crakc"])

v_controller.setEstado(visual_estado_menu)
v_controller.start()

