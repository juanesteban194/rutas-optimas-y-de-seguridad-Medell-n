import pandas as pd
import ast



class Arista:

#primera implementacion

    def __init__(self, destino:str, length: float, risk: float, name:str):
        self.destino = destino 
        self.length = length
        self.risk = risk
        self.name = name

    def costo(self, alpha:float, beta:float) -> float:
        return alpha * self.length + beta * self.risk
    
    def __repr__(self):
        return f"Arista({self.name!r}, length={self.length:.1f}, risk={self.risk:.3f})"


class Grafo:

    def __init__(self):
        self.adjacencia: dict[str, list[Arista]] = {}
        self.coordenadas: dict[str, tuple[float, float]] = {}

    def _registrar_nodo(self, nodo:str) -> None:

        if nodo not in self.coordenadas:
            lon, lat = ast.literal_eval(nodo)
            self.coordenadas[nodo] = (lat, lon)
            self.adjacencia[nodo] = []

    def _agregar_arista(self, origen:str, arista: Arista) -> None:
        self.adjacencia[origen].append(arista)

    
    def cargar_csv(self, ruta_csv:str) -> None:
        '''Lee el archivo, calcula la media de harassmentRisk, cuenta cuántos nulos hay, y los rellena.'''

        df = pd.read_csv(ruta_csv, sep =";")
        media_riesgo = df["harassmentRisk"].mean()
        nulos = df["harassmentRisk"].isna().sum()
        df["harassmentRisk"] = df["harassmentRisk"].fillna(media_riesgo)

        print(f"[Grafo] {nulos} valores nulos en harassmentRisk → "
          f"rellenados con media={media_riesgo:.4f}")
        
        #2 Recorrer cada fila y extraer los datos
        for _, fila in df.iterrows():
            origen  = fila["origin"]
            destino = fila["destination"]
            length  = float(fila["length"])
            risk    = float(fila["harassmentRisk"])
            name    = str(fila["name"])
            if name == "nan":
                name = "Calle sin nombre"
            oneway  = bool(fila["oneway"])

        #3 Registrar nodos y agregar aristas
        self._registrar_nodo(origen)
        self._registrar_nodo(destino)

        self._agregar_arista(origen, Arista(destino, length, risk, name))
        
        #4 Si la vía no es unidireccional, agrega también destino → origen con los mismos datos.
        if not oneway:
            self._agregar_arista(destino, Arista(origen, length, risk, name))

        #5 Confirmar cuánto se cargó
        print(f"[Grafo] {len(self.adjacencia)} nodos cargados")
        print(f"[Grafo] {self.total_aristas()} aristas cargadas")
        

    def vecinos(self, nodo: str) -> list[Arista]:
        return self.adjacencia.get(nodo, [])
    
    def nodo_mas_cercano(self, lat: float, lon: float) -> str:
        mejor_nodo = None
        mejor_dist = float("inf")

        for nodo, (n_lat, n_lon) in self.coordenadas.items():
            dist = (lat - n_lat) ** 2 + (lon - n_lon) ** 2
            if dist < mejor_dist:
                mejor_dist = dist
                mejor_nodo = nodo

        return mejor_nodo
    
    def existe_nodo(self, nodo: str) -> bool:
        return nodo in self.adjacencia

    def total_nodos(self) -> int:
        return len(self.adjacencia)

    def total_aristas(self) -> int:
        return sum(len(v) for v in self.adjacencia.values())