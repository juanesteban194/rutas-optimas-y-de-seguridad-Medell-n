from dataclasses import dataclass

import heapq
import time
from dataclasses import dataclass, field
from grafo import Grafo

@dataclass
class ResultadoRuta:
    algoritmo: str
    ruta: list[str]
    costo_total: float
    nodos_explorados: int
    tiempo_ms: float
    encontrada: bool
    

def greedy(grafo: Grafo, origen: str, destino: str, alpha: float, beta: float) -> ResultadoRuta:

    #1 inicializamos todo
    inicio:float = time.perf_counter()

    ruta:list[str] = [origen]
    visitados:set[str] = {origen}
    nodo_actual:str = origen
    costo_total:float = 0.0
    nodos_explorados:float = 1

    while nodo_actual != destino:

        vecinos = grafo.vecinos(nodo_actual)
        candidatos = [arista for arista in vecinos if arista.destino not in visitados]

        if not candidatos:
            tiempo_ms = (time.perf_counter() - inicio) * 1000
            return ResultadoRuta(algoritmo= "Greedy",ruta=[],costo_total=float("inf"),
                                 nodos_explorados=nodos_explorados,tiempo_ms=tiempo_ms,encontrada=False)
          

        mejor = min(candidatos, key=lambda arista: arista.costo(alpha, beta))

        costo_total += mejor.costo(alpha, beta)
        nodo_actual = mejor.destino
        visitados.add(nodo_actual)
        ruta.append(nodo_actual)
        nodos_explorados += 1

    tiempo_ms = (time.perf_counter() - inicio) * 1000
    return ResultadoRuta(
        algoritmo="Greedy",
        ruta=ruta,
        costo_total=costo_total,
        nodos_explorados=nodos_explorados,
        tiempo_ms=tiempo_ms,
        encontrada=True
        )


def bfs_costos(grafo: Grafo, origen: str, destino: str,alpha: float, beta: float) -> ResultadoRuta:

    inicio = time.perf_counter()

    heap = [(0.0, origen, [origen])]
    costo_minimo: dict[str, float] = {origen: 0.0}
    nodos_explorados = 0