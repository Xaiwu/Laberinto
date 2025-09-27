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

v_controller = VisualController(ANCHO,ALTO)
v_controller.setEstado(visual_estado_menu)
v_controller.start()
