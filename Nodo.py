class Nodo:
    def __init__(self, datos=None, siguiente=None, anterior=None):
        self.dato = datos
        self.anterior = anterior
        self.siguiente = siguiente