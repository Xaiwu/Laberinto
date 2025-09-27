class Pared:
    def __init__(self, posicion):
        self.posicion = posicion

    def mover(self, nuevas_posiciones):
        if nuevas_posiciones:
            self.posicion = nuevas_posiciones[0]