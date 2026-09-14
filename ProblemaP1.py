import sys
import heapq


def construirGrafo(numOrbitas, numPosiciones, energia, portales):
    totalNodos = numOrbitas * numPosiciones
    
    # Inicializamos el diccionario real para todos los nodos
    G = {}
    for i in range(totalNodos):
        G[i] = []
    
    # 1. Agregamos las aristas de movimiento dentro de cada orbita
    for orbita in range(numOrbitas):
        costoInterno = energia[orbita]
        for posicion in range(numPosiciones):
            nodoActual = orbita * numPosiciones + posicion
            
            # Movimiento a la izquierda (misma orbita, posicion anterior)
            if posicion > 0:
                G[nodoActual].append((nodoActual - 1, costoInterno))
            
            # Movimiento a la derecha (misma orbita, posicion siguiente)
            if posicion < numPosiciones - 1:
                G[nodoActual].append((nodoActual + 1, costoInterno))
                
    # 2. Agregamos las aristas de los portales (costo 0)
    for origenOrbita, origenPosicion, destinoOrbita, destinoPosicion in portales:
        idOrigen = (origenOrbita - 1) * numPosiciones + (origenPosicion - 1)
        idDestino = (destinoOrbita - 1) * numPosiciones + (destinoPosicion - 1)
        G[idOrigen].append((idDestino, 0))
        
    return G


# -----------------------------------------------------------------------------
# Implementación de Dijkstra vista en clase, usando el método relajar()
# -----------------------------------------------------------------------------
def relajar(u, v, peso, d, padres):
    # if d[u] + w(u, v) < d[v]:
    if d[u] + peso < d[v]:
        d[v] = d[u] + peso
        padres[v] = u
        return True
    return False


def dijkstra(G, s):
    # Inicialización de distancias
    distancia = {v: float('inf') for v in G}
    distancia[s] = 0
    padres = {v: None for v in G}

    # Q = cola de prioridad de mínimo
    Q = [(0, s)]
    heapq.heapify(Q)

    # while Q not empty:
    while Q:
        d, v = heapq.heappop(Q)

        if d > distancia[v]:
            continue

        # for u in vecindario(v):
        for u, peso in G.get(v, []):
            # if relajar(v, u):
            if relajar(v, u, peso, distancia, padres):
                # Q.decrease_key() (simulado eficientemente mediante inserción en heapq)
                heapq.heappush(Q, (distancia[u], u))

    return distancia

# -----------------------------------------------------------------------------

def leerEntrada(datos):
    if not datos:
        return []
    indice = 0
    numCasos = datos[indice]
    indice += 1

    casos = []
    for _ in range(numCasos):
        numOrbitas = datos[indice]
        numPosiciones = datos[indice + 1]
        numPortales = datos[indice + 2]
        indice += 3

        energia = datos[indice:indice + numOrbitas]
        indice += numOrbitas

        portales = []
        for _ in range(numPortales):
            origenOrbita = datos[indice]
            origenPosicion = datos[indice + 1]
            destinoOrbita = datos[indice + 2]
            destinoPosicion = datos[indice + 3]
            indice += 4
            portales.append((origenOrbita, origenPosicion, destinoOrbita, destinoPosicion))

        casos.append((numOrbitas, numPosiciones, energia, portales))
    return casos

def formatearSalida(resultados):
    lineas = []
    for resultado in resultados:
        if resultado is None or resultado == float("inf"):
            lineas.append("NO EXISTE")
        else:
            lineas.append(str(resultado))
    return "\n".join(lineas)


def main():
    datos = [int(x) for x in sys.stdin.buffer.read().split()]
    if not datos:
        return

    casos = leerEntrada(datos)
    resultados = []
    
    for numOrbitas, numPosiciones, energia, portales in casos:
        # Construimos el diccionario con todos los nodos y aristas
        G = construirGrafo(numOrbitas, numPosiciones, energia, portales)
        
        idInicio = 0
        idFin = (numOrbitas * numPosiciones) - 1
        
        # Ejecutamos el algoritmo
        distancias = dijkstra(G, idInicio)
        
        # Obtenemos la distancia al nodo final
        resultados.append(distancias.get(idFin, float("inf")))

    salida = formatearSalida(resultados)
    if salida:
        print(salida)


if __name__ == "__main__":
    main()
