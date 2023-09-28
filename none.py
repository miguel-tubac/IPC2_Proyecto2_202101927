from Nodo import Nodo

class ListaDoble:
    def __init__(self):
        self.primero = None

    def insertar(self, dato):
        if self.primero is None:
            self.primero = Nodo(datos=dato)
        else:
            actual = Nodo(datos=dato, siguiente=self.primero)
            self.primero.anterior = actual
            self.primero = actual

    def recorrer(self):
        if self.primero is None:
            return
        actual = self.primero
        while actual:
            yield actual
            actual = actual.siguiente


    def eliminar_duplicados(self):
        if self.primero is None:
            return

        actual = self.primero
        while actual:
            dato_actual = actual.dato
            siguiente = actual.siguiente
            anterior = actual.anterior

            # Buscar duplicados a partir del nodo siguiente
            duplicado = False
            while siguiente:
                if siguiente.dato == dato_actual:
                    duplicado = True
                    siguiente = siguiente.siguiente
                    if siguiente:
                        siguiente.anterior = anterior
                    if anterior:
                        anterior.siguiente = siguiente
                    else:
                        self.primero = siguiente
                else:
                    siguiente = siguiente.siguiente
                    if siguiente:
                        anterior = siguiente.anterior

            # Avanzar al siguiente nodo solo si no hubo duplicados
            if not duplicado:
                actual = actual.siguiente

lista = ListaDoble()
lista.insertar("DronY")
lista.insertar("DronW")
lista.insertar("DronX")
lista.insertar("DronA")
lista.insertar("DronW")  # Dato duplicado

lista.eliminar_duplicados()

for nodo in lista.recorrer():
    print(nodo.dato)