import os
from grafo import Grafo
from algoritmos import greedy, bfs_costos
from visualizacion import crear_mapa_base, dibujar_ruta, guardar_mapa, imprimir_tabla

# Pesos de la función de costo C(e) = α×length + β×risk
# α=1 pondera distancia en metros
# β=100 pondera riesgo — multiplicado para equilibrar escala con la distancia
ALPHA = 1
BETA  = 100

# Rutas de archivos
RUTA_CSV  = "data/calles_de_medellin_con_acoso.csv"
RUTA_MAPA = "resultados/mapa_rutas.html"

def cargar_grafo() -> Grafo:
    # Construir el grafo completo desde el dataset
    grafo = Grafo()
    grafo.cargar_csv(RUTA_CSV)
    return grafo


def pedir_punto(grafo: Grafo, nombre: str) -> str:
    print(f"\nIngresa las coordenadas del {nombre}")
    print("Formato: latitud longitud  (ejemplo: 6.2100 -75.5700)")

    # Leer y parsear la entrada del usuario
    entrada = input(">>> ").strip()
    lat, lon = map(float, entrada.split())

    # Buscar el nodo del grafo más cercano a ese punto
    nodo = grafo.nodo_mas_cercano(lat, lon)
    lat_nodo, lon_nodo = grafo.coordenadas[nodo]

    print(f"[{nombre}] nodo más cercano: {nodo}")
    print(f"[{nombre}] coordenadas reales: lat={lat_nodo:.6f}, lon={lon_nodo:.6f}")

    return nodo


def ejecutar(grafo: Grafo, origen: str, destino: str) -> None:

    print("\n[Ejecutando algoritmos...]")

    # Correr ambos algoritmos con los mismos parámetros
    resultado_greedy = greedy(grafo, origen, destino, ALPHA, BETA)
    resultado_bfs    = bfs_costos(grafo, origen, destino, ALPHA, BETA)

    # Mostrar tabla comparativa en consola
    imprimir_tabla(resultado_greedy, resultado_bfs)

    # Crear mapa base centrado entre origen y destino
    mapa = crear_mapa_base(grafo, origen, destino)

    # Dibujar cada ruta con su color — naranja greedy, azul BFS
    dibujar_ruta(mapa, grafo, resultado_greedy, color="orange")
    dibujar_ruta(mapa, grafo, resultado_bfs,    color="blue")

    # Crear carpeta resultados si no existe y guardar el mapa
    os.makedirs("resultados", exist_ok=True)
    guardar_mapa(mapa, RUTA_MAPA)


def main() -> None:
    grafo  = cargar_grafo()
    origen  = pedir_punto(grafo, "Origen")
    destino = pedir_punto(grafo, "Destino")
    ejecutar(grafo, origen, destino)


if __name__ == "__main__":
    main()