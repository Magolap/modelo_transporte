import pandas as pd
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
        self.nodos[destino][origen] = costo  # ruta bidireccional

    def dijkstra(self, inicio, fin):
        cola = [(0, inicio)]
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

# Leer CSV modificado
df = pd.read_csv("transporte.csv")

# Calcular el costo ajustado
df["costo_ajustado"] = df["costo"] + df["hora_pico"] + df["lluvia"] + df["dia_laboral"] + df["retraso"]

# Crear el grafo
grafo = Grafo()
for _, fila in df.iterrows():
    grafo.agregar_ruta(fila["origen"], fila["destino"], fila["costo_ajustado"])

# Buscar la mejor ruta
inicio = "A"
fin = "G"
ruta = grafo.dijkstra(inicio, fin)
print(f"\nRuta más eficiente desde {inicio} hasta {fin}: {ruta}")

# Mostrar detalles por tramo
print("\nDetalle de factores por tramo:")
for i in range(len(ruta) - 1):
    tramo = df[((df["origen"] == ruta[i]) & (df["destino"] == ruta[i+1])) | 
               ((df["origen"] == ruta[i+1]) & (df["destino"] == ruta[i]))]
    if not tramo.empty:
        fila = tramo.iloc[0]
        print(f"De {fila['origen']} a {fila['destino']} | Costo base: {fila['costo']} | "
              f"Hora pico: {fila['hora_pico']} | Lluvia: {fila['lluvia']} | "
              f"Día laboral: {fila['dia_laboral']} | Retraso: {fila['retraso']} | "
              f"Costo ajustado: {fila['costo_ajustado']}")
