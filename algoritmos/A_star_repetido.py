import heapq
import random

class ARepetido:
    def __init__(self, inicio, salidas, laberinto, prob_mover_paredes=0.2, debug=False, modo='normal', vision=1):
        self.salidas_totales = [s for s in salidas]
        self.posicion = inicio
        self.lab = laberinto
        self.mapa = {}                 # (x,y) -> 'libre' | 'pared' | 'salida'
        self.salidas_falsas = set()
        self.encontro_real = False
        self.prob_mover_paredes = prob_mover_paredes
        self.plan_actual = []          # lista de posiciones (no incluye posición actual)
        self.debug = debug
        self.pasos = 0
        self.modo = modo      # 'normal' o 'exploracion'
        self.vision = vision  # nivel de visión del agente

    # Heurística Manhattan
    def heuristica(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    # Genera vecinos válidos (dentro del laberinto)
    def vecinos(self, pos):
        x, y = pos
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            v = (x+dx, y+dy)
            if self.lab.en_rango(v):
                yield v

    # Actualiza el mapa parcial del agente según su percepción
    def percibir(self):
            if self.modo == 'exploracion':
                vision = self.vision
                x0, y0 = self.posicion
                for dx in range(-vision, vision+1):
                    for dy in range(-vision, vision+1):
                        x, y = x0 + dx, y0 + dy
                        pos = (x, y)
                        if not self.lab.en_rango(pos):
                            continue
                        if self.lab.es_pared(pos):
                            self.mapa[pos] = 'pared'
                        elif self.lab.es_salida(pos):
                            print(f"[DEBUG] Percibida salida en {pos}")
                            self.mapa[pos] = 'salida'
                        else:
                            self.mapa[pos] = 'libre'
            elif self.modo == 'normal':
                # Solo percibe las casillas vecinas inmediatas
                for v in self.vecinos(self.posicion):
                    if self.lab.es_pared(v):
                        self.mapa[v] = 'pared'
                    elif self.lab.es_salida(v):
                        self.mapa[v] = 'salida'
                    else:
                        self.mapa[v] = 'libre'
            # Marca la posición actual
            if self.lab.es_salida(self.posicion):
                self.mapa[self.posicion] = 'salida'
            else:
                self.mapa[self.posicion] = 'libre'

    # Algoritmo A* multi-meta sobre el mapa parcial del agente
    def _a_star(self, origen, metas):
        if not metas:
            return None
        metas_set = set(metas)
        openh = []
        g = {origen: 0}
        parent = {}
        # h = min distancia a cualquier meta
        h0 = min(self.heuristica(origen, m) for m in metas_set)
        heapq.heappush(openh, (h0, 0, origen))
        cerrados = set()
        while openh:
            f, gc, s = heapq.heappop(openh)
            if s in cerrados:
                continue
            cerrados.add(s)
            if s in metas_set:
                # Reconstruye el camino desde origen hasta la meta encontrada
                camino = []
                cur = s
                while cur != origen:
                    camino.append(cur)
                    cur = parent[cur]
                camino.reverse()
                return camino
            for v in self.vecinos(s):
                # Si sabemos que es pared, no expandimos
                if self.mapa.get(v) == 'pared':
                    continue
                ng = gc + 1
                if ng < g.get(v, 1e12):
                    g[v] = ng
                    parent[v] = s
                    h = min(self.heuristica(v, m) for m in metas_set)
                    heapq.heappush(openh, (ng + h, ng, v))
        return None
    
    # Encuentra fronteras: celdas conocidas adyacentes a celdas desconocidas
    def _fronteras(self):
        """Devuelve celdas conocidas libres/salida adyacentes a al menos una celda desconocida."""
        fr = set()
        for (c, tipo) in self.mapa.items():
            if tipo in ('libre', 'salida'):
                for v in self.vecinos(c):
                    if v not in self.mapa:
                        fr.add(c)
                        break
        return fr

    # Decide el plan a seguir: hacia salida, frontera o explora
    def planificar(self):
        # print(f"[DEBUG] Mapa actual: {self.mapa}")
        if self.modo == 'normal':
            # Planea hacia cualquier salida conocida (no descartada como falsa)
            candidatas = [s for s in self.salidas_totales if s not in self.salidas_falsas]
            # print(f"[DEBUG] (NORMAL) Candidatas: {candidatas}")
            if candidatas:
                camino = self._a_star(self.posicion, candidatas)
                if camino:
                    self.plan_actual = camino
                    if self.debug:
                        print(f"[DEBUG] (NORMAL) Plan hacia salida {camino[-1]} len={len(camino)}")
                    return
        elif self.modo == "exploracion":
            # Planea solo hacia salidas percibidas en el mapa
            # 1. Salidas candidatas visibles (no descartadas) y conocidas
            candidatas_visibles = [s for s in self.mapa.keys() 
                                if s not in self.salidas_falsas and self.mapa.get(s) == 'salida']
            if candidatas_visibles:
                camino = self._a_star(self.posicion, candidatas_visibles)
                if camino:
                    self.plan_actual = camino
                    if self.debug:
                        print(f"[DEBUG] Plan hacia salida {camino[-1]} len={len(camino)}")
                    return

            # 2. Explorar frontera (expansión del conocimiento)
            fronteras = list(self._fronteras())
            if fronteras:
                camino = self._a_star(self.posicion, fronteras)
                if camino:
                    self.plan_actual = camino
                    if self.debug:
                        print(f"[DEBUG] Plan exploración frontera len={len(camino)}")
                    return

            # 3. Sin plan
            self.plan_actual = []
            if self.debug:
                print("[DEBUG] No se pudo planificar (sin metas ni fronteras).")

    # Intenta mover al destino, actualiza el mapa si hay pared dinámica
    def _mover_a(self, destino):
        if self.lab.es_pared(destino):
            # Apareció/movió una pared dinámica
            self.mapa[destino] = 'pared'
            if self.debug:
                print(f"[DEBUG] Movimiento bloqueado por pared dinámica en {destino}")
            return False
        self.posicion = destino
        # Si es salida la percepción futura la volverá a etiquetar; aquí asume libre
        if destino not in self.mapa or self.mapa[destino] != 'salida':
            self.mapa[destino] = 'libre'
        return True

    # Ejecuta un ciclo de percepción, planificación y movimiento
    def paso(self):
        if self.encontro_real:
            return False, "Terminado"

        self.percibir()

        # Si estamos sobre una salida 
        if self.lab.es_salida(self.posicion):
            if self.lab.es_salida_real(self.posicion):
                self.encontro_real = True
                return False, "W" # WIN
            else:
                # Salida falsa descubierta
                self.salidas_falsas.add(self.posicion)
                if self.debug:
                    print(f"[DEBUG] Salida falsa en {self.posicion}, descartada.")
                # Forzar replanteo
                self.plan_actual = []

        # Si no hay plan o se agotó, planificar
        if not self.plan_actual:
            self.planificar()
            if not self.plan_actual:
                # Si no hay plan, intenta moverse a un vecino libre al azar
                candidatos = [v for v in self.vecinos(self.posicion)
                              if self.mapa.get(v) != 'pared']
                if candidatos:
                    destino = random.choice(candidatos)
                    self._mover_a(destino)
                    # mover paredes luego
                    self.lab.mover_paredes(self.prob_mover_paredes)
                    return True, "ESP" # EXPLORANDO
                self.lab.mover_paredes(self.prob_mover_paredes)
                return True, "SA" # SIN ACCION (atrapado)

        # Ejecutar siguiente paso del plan
        if self.plan_actual:
            destino = self.plan_actual.pop(0)
            exito = self._mover_a(destino)
            if not exito:
                # Pared dinámica bloqueó el plan
                self.plan_actual = []
            # Dinámica
            self.lab.mover_paredes(self.prob_mover_paredes)

        self.pasos += 1
        return True, "A" # AVANZANDO
    
    # Ejecuta el ciclo completo hasta terminar
    def run(self, interactivo=True):
        while True:
            self.lab.mostrar(self.posicion)
            cont, msg = self.paso()
            # Mostrar el laberinto y la posición del agente
            print(f"\nPaso={self.pasos} Pos={self.posicion} Msg={msg}")
            if interactivo:
                input("Presiona Enter para continuar al siguiente paso...")  # Pausa
            if not cont:
                print(msg)
                break
        if self.encontro_real:
            print(f"Éxito en {self.pasos} pasos.")
        else:
            print("Fallo (no encontró salida real).")
