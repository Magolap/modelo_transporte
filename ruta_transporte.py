import heapq

class Grafo:
    def __init__(self):
        self.nodos = {}

    def agregar_ruta(self, origen, destino, costo):
        if origen not in self.nodos:
            self.nodos[origen] = {}
        if destino not in self.nodos:
            self.nodos[destino] = {}
        self.nodos[origen][destino] = costo
        self.nodos[destino][origen] = costo  # Conexión bidireccional

    def dijkstra(self, inicio, fin):
        cola = [(0, inicio)]  # (costo acumulado, nodo actual)
        visitados = {}
        rutas = {}

        while cola:
            costo_actual, nodo_actual = heapq.heappop(cola)

            if nodo_actual in visitados:
                continue

            visitados[nodo_actual] = costo_actual
            if nodo_actual == fin:
                break

            for vecino, costo in self.nodos[nodo_actual].items():
                if vecino not in visitados:
                    heapq.heappush(cola, (costo_actual + costo, vecino))
                    rutas[vecino] = nodo_actual

        return self.construir_camino(rutas, inicio, fin)

    def construir_camino(self, rutas, inicio, fin):
        camino = []
        nodo = fin
        while nodo != inicio:
            camino.append(nodo)
            nodo = rutas.get(nodo, inicio)
        camino.append(inicio)
        return list(reversed(camino))

# Definimos la red de transporte
grafo = Grafo()
grafo.agregar_ruta("A", "B", 4)
grafo.agregar_ruta("A", "E", 2)
grafo.agregar_ruta("B", "C", 5)
grafo.agregar_ruta("C", "D", 3)
grafo.agregar_ruta("E", "F", 6)
grafo.agregar_ruta("F", "G", 2)
grafo.agregar_ruta("B", "F", 1)
grafo.agregar_ruta("C", "G", 4)

# Ejemplo de búsqueda de ruta
inicio, fin = "A", "B"
ruta_optima = grafo.dijkstra(inicio, fin)
print(f"Mejor ruta de {inicio} a {fin}: {ruta_optima}")
