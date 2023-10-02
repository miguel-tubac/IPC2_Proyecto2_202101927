import tkinter as tk

class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()

        self.menu_principal = tk.Menu(self)

        # Crear un submenú dinámico
        self.submenu_dinamico = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Submenú Dinámico", menu=self.submenu_dinamico)

        # Obtener opciones para el submenú (pueden ser obtenidas dinámicamente)
        opciones = ["Rojo", "Verde", "Azul"]

        # Agregar opciones al submenú
        for opcion in opciones:
            # Crear un nuevo submenú para cada opción
            submenu_tamanos = tk.Menu(self.submenu_dinamico, tearoff=0)
            submenu_tamanos.add_command(label="Pequeño", command=lambda: self.seleccionar_tamano("Pequeño"))
            submenu_tamanos.add_command(label="Mediano", command=lambda: self.seleccionar_tamano("Mediano"))
            submenu_tamanos.add_command(label="Grande", command=lambda: self.seleccionar_tamano("Grande"))

            # Agregar la opción principal al submenú dinámico con el nuevo submenú adjunto
            self.submenu_dinamico.add_cascade(label=opcion, menu=submenu_tamanos)

        # Configurar el menú principal
        self.config(menu=self.menu_principal)

    def seleccionar_color(self, color):
        # Acción a realizar cuando se selecciona una opción del submenú
        print(f"Color seleccionado: {color}")

    def seleccionar_tamano(self, tamano):
        # Acción a realizar cuando se selecciona una opción del submenú de tamaños
        print(f"Tamaño seleccionado: {tamano}")

# Crear la instancia de la ventana
ventana = Ventana()

# Iniciar el bucle principal
ventana.mainloop()
