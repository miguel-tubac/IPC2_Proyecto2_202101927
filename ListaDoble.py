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

    def borrar_todos(self):
        self.primero = None

    # def eliminar(self,usuario):
    #     actual = self.primero
    #     while actual != None:
    #         if actual.nota.usuario == usuario:
    #             if actual.anterior != None:
    #                 if actual.siguiente != None:
    #                     actual.anterior.siguiente = actual.siguiente
    #                     actual.siguiente.anterior = actual.anterior
    #                     actual.siguiente = None
    #                     actual.anterior = None
    #                 else:
    #                     actual.anterior.siguiente = None
    #                     actual.anterior = None
    #             else:
    #                 if actual.siguiente != None:
    #                     self.primero = actual.siguiente
    #                     actual.siguiente.anterior = None
    #                 else:
    #                     self.primero = None
    #             return True
    #         else:
    #             actual = actual.siguiente
    #     return False
        

