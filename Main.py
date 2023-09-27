import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

from LecturaXML import ConfigParser

class ScrollText(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(
            self,
            bg="#f8f9fa",
            foreground="#343a40",
            insertbackground="#3b5bdb",
            selectbackground="blue",
            width=140,
            height=38,
            font=("Courier New", 10),
        )
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto 2 - IPC2")
        self.geometry("1200x650+70+20")
        self.scroll = ScrollText(self)
        self.scroll.pack()

        # Almacenar la path
        self.path = None

        #Datos para almacenar y borrar la lista doble enlazada
        self.lista_drones = None
        self.lista_sistemas_drones = None
        self.lista_mensajes = None

        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.filemenu2 = Menu(self.menu)

        self.menu.add_command(label="Salir", command=self.quit)

        self.menu.add_command(label="a. Inicializacion", command=self.reiniciarSistema)
        self.menu.add_command(label="b. Cargar(Archivo)", command=self.open_file)
        self.menu.add_command(label="c. Generar(Archivo)", command=self.mostrarPrueba)

        self.menu.add_cascade(label="d. Gestion(Drones)", menu=self.filemenu)
        self.filemenu.add_command(label="a. Listado(Drones)")
        self.filemenu.add_command(label="b. Agregar(Dron)")

        self.menu.add_command(label="e. ListaDrones(Grafica)")

        self.menu.add_cascade(label="f. Gestion(Mensajes)", menu=self.filemenu2)
        self.filemenu2.add_command(label="a. Listado(Mensajes)")
        self.filemenu2.add_separator()
        self.filemenu2.add_command(label="i. Seleccionar(Mensaje)")
        self.filemenu2.add_command(label="ii. Mostrar(sistema)")
        self.filemenu2.add_command(label="iii. Grafica(Instruciones)")

        self.menu.add_command(label="g. Ayuda")

    def open_file(self):
        filepath = askopenfilename(
            filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        # Se muestra la direcion del archivo en la ventana
        self.title(f"Proyecto 2 - IPC2 - {filepath}")
        self.path = filepath
        


    def mostrarPrueba(self):
        if not self.path:
            # mensaje de error que ya se reinicio el sistema
            self.scroll.delete(1.0,tk.END)
            return
        # Se recorre la listadoble y se almcena la informacion en una variable para mostrarla en el text area
        parser = ConfigParser(self.path)

        self.lista_drones = parser.get_lista_drones()
        mostrar = "--------------------------------------\n"
        mostrar += "           Drones:    \n"
        for elemento in self.lista_drones.recorrer():
            mostrar += elemento.dato.nombre+"\n"
        mostrar +="--------------------------------------\n"

        self.lista_sistemas_drones = parser.get_lista_sistemas_drones()
        mostrar +="     Lista de Sistemas de Drones:  \n"
        for sistema in self.lista_sistemas_drones.recorrer():
            mostrar += "nombre: " + sistema.dato.nombre + "\n altura_maxima: " + sistema.dato.alturaMaxima + "\n cantidad_drones: " + sistema.dato.cantidadDrones + "\n"                
            for contenido in sistema.dato.contenido.recorrer():
                mostrar +="dron: "+ contenido.dato.dron+"\n"
                for altura in contenido.dato.alturas.recorrer():
                   mostrar +="altura - valor= "+ altura.dato.valor +" Letra: "+ altura.dato.letra +"\n"
        mostrar +="--------------------------------------\n"

        self.lista_mensajes = parser.get_lista_mensajes()
        mostrar +="     Lista de Mensajes:  \n"
        for mensaje in self.lista_mensajes.recorrer():
            mostrar += "nombre: "+ mensaje.dato.nombre + "\n sistemaDrones: "+ mensaje.dato.sistemaDrones + "\n"
            for instruc in mensaje.dato.instrucciones.recorrer():
                mostrar += "instruccion - dron: "+ instruc.dato.dron + " Instrucion: " + instruc.dato.valorInstrucion + "\n"
        mostrar +="--------------------------------------"
        self.scroll.insert(tk.END, mostrar)


    def reiniciarSistema(self):
        self.lista_drones.borrar_todos()
        self.lista_sistemas_drones.borrar_todos()
        self.lista_mensajes.borrar_todos()

        self.path = None
        self.mostrarPrueba()
    

app = Ventana()
app.mainloop()