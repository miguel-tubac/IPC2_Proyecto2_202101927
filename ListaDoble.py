from Nodo import Nodo


class ListaDoble:
    def __init__(self):
        self.primero = None

    def insertar(self, nota):
        if self.primero is None:
            self.primero = Nodo(datos=nota)
        else:
            actual= Nodo(datos=nota, siguiente=self.primero)
            self.primero.anterior = actual
            self.primero = actual

    def recorrer(self):
        if self.primero is None:
            return
        actual = self.primero
        while actual:
            yield actual
            actual = actual.siguiente
            

