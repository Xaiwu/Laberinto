from Logica.laberinto import Laberinto
from Visual.visual_controller import VisualController
from Visual.visual_laberinto import LaberintoVisual

# Configuración
ANCHO, ALTO = 600, 600
TAM = 25
TAM_CELDA = ANCHO // TAM 

l = Laberinto(TAM,10,10)
l.mostrar()
visual_l = LaberintoVisual(l,TAM_CELDA)

v_controller = VisualController(ANCHO,ALTO)
v_controller.setEstado(visual_l)
v_controller.start()
