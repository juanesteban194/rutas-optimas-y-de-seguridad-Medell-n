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
    

#V = nodos del grafo (27.671)
#E = aristas totales (126.729)
#E_max = máximo de aristas que sale de un nodo

def greedy(grafo: Grafo, origen: str, destino: str, alpha: float, beta: float) -> ResultadoRuta:

    #1 inicializamos todo
    inicio:float = time.perf_counter() #O1

    '''O(V) pasa por todos los nodos'''
    ruta:list[str] = [origen] #O1
    '''O(V) visita todos los nodos'''
    visitados:set[str] = {origen}#O1
    nodo_actual:str = origen #O1
    costo_total:float = 0.0 #O1
    nodos_explorados:int = 1 #01
   
    while nodo_actual != destino: #0V EN EL PEOR DE LOS CASOS RECORRE TODOOS LOS NODOS DEL GRAFO ANTES DE QUEDAR ATRAPADO

        vecinos = grafo.vecinos(nodo_actual) #01 CONSULTAR EN UN dict ES 01
        '''O(E_max)- lista temporal que se recrea en cada iteración'''
        candidatos = [arista for arista in vecinos if arista.destino not in visitados] #O(E_max)para el for, 
                                                                                       #01 en not visitados ya que es un set

        if not candidatos:
            tiempo_ms = (time.perf_counter() - inicio) * 1000
            return ResultadoRuta(algoritmo= "Greedy",ruta=[],costo_total=float("inf"),
                                 nodos_explorados=nodos_explorados,tiempo_ms=tiempo_ms,encontrada=False)
          
        #O(E_max) recorre todos los candidatos una vez
        mejor_arista = min(candidatos, key=lambda arista: arista.costo(alpha, beta))

        #O1 operaciones en variables simples
        costo_total += mejor_arista.costo(alpha, beta) #O1 espacial-variables simples
        nodo_actual = mejor_arista.destino #O1 espacial-variables simples
        visitados.add(nodo_actual)
        ruta.append(nodo_actual)
        nodos_explorados += 1 #O1 espacial-variables simples

    #01
    tiempo_ms = (time.perf_counter() - inicio) * 1000
    return ResultadoRuta(
        algoritmo="Greedy",
        ruta=ruta,
        costo_total=costo_total,
        nodos_explorados=nodos_explorados,
        tiempo_ms=tiempo_ms,
        encontrada=True
        )

#O(E_max)*O(V)+O(1) = O(E_max*V)
#Espacial: [ O(1)+O(1)+O(1) + O(E_max)]+[O(V)+O(V)] = O(V)

def bfs_costos(grafo: Grafo, origen: str, destino: str,alpha: float, beta: float) -> ResultadoRuta:

    inicio = time.perf_counter()

    '''O(E) contiene una entrada por cada arista explorada'''
    heap = [(0.0, origen, [origen])] #O(1)
    '''O(V)  una entrada por nodo'''
    costo_minimo: dict[str, float] = {origen: 0.0} #O(1)
    nodos_explorados = 0 #O(1)

    while heap: #O(v+E)
        costo_actual, nodo_actual, camino = heapq.heappop(heap) #O(log len(heapq)) -> O(log E)
        nodos_explorados += 1 #O(1)

        if nodo_actual == destino: #O(1)
            tiempo_ms = (time.perf_counter() - inicio) * 1000 #O(1)
            return ResultadoRuta(
                algoritmo="BFS Adaptado",
                ruta=camino,
                costo_total=costo_actual,
                nodos_explorados=nodos_explorados,
                tiempo_ms=tiempo_ms,
                encontrada=True
            )

        if costo_actual > costo_minimo.get(nodo_actual, float("inf")): #O(1)consulta en diccionario. Esta es la poda 
                                                       #descarta entradas obsoletas de ariastas del heap sin explorar vecinos
            continue
        
        #[ [ [(O(log E) * O(V)]* O(1)] +O(1)] * O(E_max) = O(v * E_max* log E)
        for arista in grafo.vecinos(nodo_actual): #O(E_max)
            nuevo_costo = costo_actual + arista.costo(alpha, beta) #O(1)

            if nuevo_costo < costo_minimo.get(arista.destino, float("inf")): #O(1) consulta y escritura en diccionario.
                costo_minimo[arista.destino] = nuevo_costo
                '''O(V) cada camino almacenado en el heap puede tener hasta V nodos. Y hay hasta E entradas en el heap, 
                entonces en el peor caso esto es O(V x E)'''
                heapq.heappush(heap, (nuevo_costo, arista.destino, camino + [arista.destino]))# O(log len(heapq)*O(V) porque copia la lista

    tiempo_ms = (time.perf_counter() - inicio) * 1000
    #no encontramos la ruta
    return ResultadoRuta(
        algoritmo="BFS Adaptado",
        ruta=[],
        costo_total=float("inf"),
        nodos_explorados=nodos_explorados,
        tiempo_ms=tiempo_ms,
        encontrada=False
            )
    
# { [ [(O(log E) * O(V))*O(1)] + O(1)] *O(E_max) ] + O(1) + O(1)} * O(V+E) + O(1)
# { O(v * E_max* log E) * O(V+E) = O(E*v * E_max* log E) -> E>V

#Espacial: O(V*E) + O(V) + O(E) = O(V*E)

