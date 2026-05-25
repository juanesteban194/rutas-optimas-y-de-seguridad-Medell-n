import folium
from grafo import Grafo
from algoritmos import ResultadoRuta


def crear_mapa_base(grafo: Grafo, origen: str, destino: str) -> folium.Map:

    # Extraer coordenadas numéricas de origen y destino desde el diccionario del grafo
    # coordenadas guarda tuplas (lat, lon)
    lat_origen, lon_origen = grafo.coordenadas[origen]
    lat_destino, lon_destino = grafo.coordenadas[destino]

    # Calcular el punto medio entre origen y destino
    # Folium necesita un centro para saber dónde enfocar la vista al abrir el mapa
    centro_lat = (lat_origen + lat_destino) / 2
    centro_lon = (lon_origen + lon_destino) / 2

    # Crear el mapa base con OpenStreetMap como fondo
    # zoom_start=14 es nivel de barrio, suficiente para ver calles individuales
    mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=14)

    # Agregar marcador verde en el origen
    # popup es el texto al hacer clic, icon usa iconos Bootstrap incluidos en folium
    folium.Marker(
        location=[lat_origen, lon_origen],
        popup="Origen",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(mapa)

    # Agregar marcador rojo en el destino
    # El contraste verde/rojo hace inmediatamente visible inicio y fin
    folium.Marker(
        location=[lat_destino, lon_destino],
        popup="Destino",
        icon=folium.Icon(color="red", icon="stop")
    ).add_to(mapa)

    # Devolver el mapa para que dibujar_ruta le agregue las líneas encima
    return mapa


def dibujar_ruta(mapa: folium.Map, grafo: Grafo,
                 resultado: ResultadoRuta,
                 color: str) -> None:

    # Si el algoritmo no encontró ruta no hay nada que dibujar
    if not resultado.encontrada:
        return

    # Recorrer la ruta en pares consecutivos: ruta[0]→ruta[1], ruta[1]→ruta[2], ...
    
    for i in range(len(resultado.ruta) - 1):
        nodo_origen  = resultado.ruta[i]
        nodo_destino = resultado.ruta[i + 1]

        # Traducir los nodos del par a coordenadas numéricas
        # Folium no entiende strings de coordenadas, necesita números
        lat_a, lon_a = grafo.coordenadas[nodo_origen]
        lat_b, lon_b = grafo.coordenadas[nodo_destino]

        # Buscar la arista entre este par de nodos para mostrar sus datos en el popup
        # next(..., None) devuelve None si no la encuentra en lugar de lanzar un error
        arista_actual = next(
            (a for a in grafo.vecinos(nodo_origen) if a.destino == nodo_destino),
            None
        )

        # Construir el texto del popup con los datos reales del tramo
        # Si no se encontró la arista mostrar solo el nombre del algoritmo como fallback
        if arista_actual:
            popup_texto = (
                f"<b>Algoritmo:</b> {resultado.algoritmo}<br>"
                f"<b>Calle:</b> {arista_actual.name}<br>"
                f"<b>Longitud:</b> {arista_actual.length:.1f} m<br>"
                f"<b>Riesgo:</b> {arista_actual.risk:.3f}<br>"
                f"<b>Costo tramo:</b> {arista_actual.costo(1, 100):.2f}"
            )
        else:
            popup_texto = f"Algoritmo: {resultado.algoritmo}"

        # Dibujar el segmento de línea entre los dos puntos del par
        # weight=4 es grosor en píxeles, opacity=0.8 deja ver el mapa debajo
        # color viene como parámetro desde main.py
        folium.PolyLine(
            locations=[[lat_a, lon_a], [lat_b, lon_b]],
            color=color,
            weight=4,
            opacity=0.8,
            popup=folium.Popup(popup_texto, max_width=250)
        ).add_to(mapa)


def guardar_mapa(mapa: folium.Map, ruta_archivo: str) -> None:
    # Serializar el mapa a HTML y guardarlo en disco
    mapa.save(ruta_archivo)
    print(f"[Mapa] guardado en {ruta_archivo}")


def imprimir_tabla(resultado_greedy: ResultadoRuta,
                   resultado_bfs: ResultadoRuta) -> None:

    # Encabezado de la tabla
    print("\n" + "=" * 65)
    print(f"{'COMPARACIÓN DE ALGORITMOS':^65}")
    print("=" * 65)
    encabezado = f"{'Métrica':<25} {'Greedy':>18} {'BFS Adaptado':>18}"
    print(encabezado)
    print("-" * 65)

    # Función interna para imprimir una fila con formato alineado
    # :<25 alinea a la izquierda, :>18 alinea a la derecha
    def fila(metrica: str, val_g: str, val_b: str) -> None:
        print(f"{metrica:<25} {val_g:>18} {val_b:>18}")

    # Fila 1: si cada algoritmo encontró ruta
    fila("Encontrada",
         "Sí" if resultado_greedy.encontrada else "No",
         "Sí" if resultado_bfs.encontrada else "No")

    # Fila 2: cuántos nodos tiene la ruta encontrada
    fila("Nodos en ruta",
         str(len(resultado_greedy.ruta)),
         str(len(resultado_bfs.ruta)))

    # Fila 3: costo total acumulado de la ruta — ∞ si no encontró
    fila("Costo total",
         f"{resultado_greedy.costo_total:.2f}" if resultado_greedy.encontrada else "∞",
         f"{resultado_bfs.costo_total:.2f}"    if resultado_bfs.encontrada    else "∞")

    # Fila 4: cuántos nodos procesó internamente cada algoritmo
    fila("Nodos explorados",
         str(resultado_greedy.nodos_explorados),
         str(resultado_bfs.nodos_explorados))

    # Fila 5: tiempo de ejecución en milisegundos
    fila("Tiempo (ms)",
         f"{resultado_greedy.tiempo_ms:.2f}",
         f"{resultado_bfs.tiempo_ms:.2f}")

    print("=" * 65 + "\n")