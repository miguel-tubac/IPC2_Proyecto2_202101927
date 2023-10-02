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

    def ordenar_alfabeticamente(self):
        if self.primero is None:
            return

        ordenado = False
        while not ordenado:
            ordenado = True
            actual = self.primero
            while actual.siguiente is not None:
                siguiente = actual.siguiente
                if ord(actual.dato.nombre[-1]) > ord(siguiente.dato.nombre[-1]):
                    actual.dato, siguiente.dato = siguiente.dato, actual.dato
                    ordenado = False
                actual = siguiente
    
    def ordenar_alfabeticamenteListaMensajes(self):
        if self.primero is None:
            return

        ordenado = False
        while not ordenado:
            ordenado = True
            actual = self.primero
            while actual.siguiente is not None:
                siguiente = actual.siguiente
                if ord(actual.dato.nombre[0]) > ord(siguiente.dato.nombre[0]):
                    actual.dato, siguiente.dato = siguiente.dato, actual.dato
                    ordenado = False
                actual = siguiente

    def eliminar_duplicados(self):
        if self.primero is None:
            return

        actual = self.primero
        while actual:
            dato_actual = actual.dato.nombre
            siguiente = actual.siguiente
            anterior = actual.anterior

            # Buscar duplicados a partir del nodo siguiente
            duplicado = False
            while siguiente:
                if siguiente.dato.nombre == dato_actual:
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
        

