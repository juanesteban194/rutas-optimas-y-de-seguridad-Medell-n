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

