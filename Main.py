import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename, asksaveasfilename

from LecturaXML import ConfigParser
from ListaDoble import ListaDoble

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
        # Con esta linea activo el text area por si deseo despues desactivarlo:
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
        # Contar las veces de repeticion del boton Listado De Drones
        self.candtidadDeClicks = 0

        # Validacion de archivos concatenados
        self.datosConcatenados = False

        #Datos para almacenar y borrar la lista doble enlazada
        self.lista_drones1 = None
        self.lista_drones2 = None
        self.lista_sistemas_drones = None
        self.lista_mensajes = None

        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.filemenu2 = Menu(self.menu)

        self.menu.add_command(label="Salir", command=self.quit)

        self.menu.add_command(label="a. Inicializar", command=self.reiniciarSistema)
        self.menu.add_command(label="b. Cargar(Archivo)", command=self.open_file)
        self.menu.add_command(label="c. Generar(Archivo)")

        self.menu.add_cascade(label="d. Gestion(Drones) ▼", menu=self.filemenu)
        self.filemenu.add_command(label="a. Listado(Drones)",command=self.mostrarDronesEnOrdenAlfabetico)
        self.filemenu.add_command(label="b. Agregar(Dron)", command=self.abrir_ventanaIngresarDron)

        self.menu.add_command(label="e. ListaDrones(Grafica)")

        self.menu.add_cascade(label="f. Gestion(Mensajes) ▼", menu=self.filemenu2)
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
        if (self.path is not None) and (self.path != filepath):
            # Aqui se valida que sea la segunda vez que se habre el explorador de archivos 
            self.datosConcatenados = True
            
        # Se almacena la path
        self.path = filepath
        # Se muestra la direcion del archivo en la ventana
        self.title(f"Proyecto 2 - IPC2 - {filepath}")
        # Mensaje de ingreso de archivo correcto
        self.mostrar_infoIngresoArchivo()
        
    def mostrarDronesEnOrdenAlfabetico(self):
        if not self.path:
            # mensaje de error que ya se reinicio el sistema
            self.scroll.delete(1.0,tk.END)
            return
        if self.candtidadDeClicks == 0:
            # Esto es para borrar y dejar limpia el text area 
            self.scroll.delete(1.0,tk.END)
            # Se recorre la listadoble y se almcena la informacion en una variable para mostrarla en el text area
            parser = ConfigParser(self.path)

            self.lista_drones1 = parser.get_lista_drones()
            self.lista_drones1.eliminar_duplicados()
            self.lista_drones1.ordenar_alfabeticamente()
            mostrar = "--------------------------------------\n"
            mostrar += "    Drones En Orden Alfabetico:    \n"
            for elemento in self.lista_drones1.recorrer():
                mostrar += elemento.dato.nombre+"\n"
            
            self.lista_sistemas_drones = parser.get_lista_sistemas_drones()
            # mostrar +="     Lista de Sistemas de Drones:  \n"
            # for sistema in self.lista_sistemas_drones.recorrer():
            #     mostrar += "nombre: " + sistema.dato.nombre + "\n altura_maxima: " + sistema.dato.alturaMaxima + "\n cantidad_drones: " + sistema.dato.cantidadDrones + "\n"                
            #     for contenido in sistema.dato.contenido.recorrer():
            #         mostrar +="dron: "+ contenido.dato.dron+"\n"
            #         for altura in contenido.dato.alturas.recorrer():
            #            mostrar +="altura - valor= "+ altura.dato.valor +" Letra: "+ altura.dato.letra +"\n"
            # mostrar +="--------------------------------------\n"

            self.lista_mensajes = parser.get_lista_mensajes()
            # mostrar +="     Lista de Mensajes:  \n"
            # for mensaje in self.lista_mensajes.recorrer():
            #     mostrar += "nombre: "+ mensaje.dato.nombre + "\n sistemaDrones: "+ mensaje.dato.sistemaDrones + "\n"
            #     for instruc in mensaje.dato.instrucciones.recorrer():
            #         mostrar += "instruccion - dron: "+ instruc.dato.dron + " Instrucion: " + instruc.dato.valorInstrucion + "\n"
            # mostrar +="--------------------------------------"
            self.scroll.insert(tk.END, mostrar)
            self.candtidadDeClicks +=1

        if self.datosConcatenados:
            # Esto es para borrar y dejar limpia el text area 
            self.scroll.delete(1.0,tk.END)
            # Instancia de la lectura de xml
            parser = ConfigParser(self.path)
            # Almacena los nuevos datos ingresados 
            self.lista_drones2 = parser.get_lista_drones()
            self.lista_drones2.eliminar_duplicados()
            self.lista_drones2.ordenar_alfabeticamente() # Esto es opcional
            # Aqui se unen las dos listasdobles:
            listaUnida =  self.unir_listas_dobles(lista1=self.lista_drones1, lista2=self.lista_drones2)
            listaUnida.eliminar_duplicados()
            listaUnida.ordenar_alfabeticamente()
            # Recorrer y mostrar la lista unida
            mostrar = "--------------------------------------\n"
            mostrar += "    Drones En Orden Alfabetico:    \n"
            for elemento in listaUnida.recorrer():
                mostrar += elemento.dato.nombre+"\n"
            # Lo inserta en el area de texto:
            self.scroll.insert(tk.END, mostrar)
            # Esto es por si se desea ingresar una tercera lista y asi sucesivamente 
            self.lista_drones1 = listaUnida
        else:
            pass


    def reiniciarSistema(self):
        # Borramos la direcion del archivo para que no pueda acceder
        self.path = None
        # Borramos las dos listas doblemente enlazadas
        self.lista_drones1 = None
        self.lista_drones2 = None
        # Inicializamos la variable que hace que se unan las dos listas enlazadas
        self.datosConcatenados = False
        # Esto es para borar los datos del texArea
        self.mostrarDronesEnOrdenAlfabetico()
        # Esto es para que se inicie de cero el almacenamiento de datos
        self.candtidadDeClicks = 0
        # Muestra el mensaje emergente 
        self.mostrar_infoReinicio()

    def unir_listas_dobles(self, lista1, lista2):
        nueva_lista = ListaDoble()
        # Recorre la primera lista y agrega sus elementos a la nueva lista
        for nodo in lista1.recorrer():
            nueva_lista.insertar(nodo.dato)
        # Recorre la segunda lista y agrega sus elementos a la nueva lista
        for nodo in lista2.recorrer():
            nueva_lista.insertar(nodo.dato)
        return nueva_lista

    # Funciones de INgreso de Texto:
    def abrir_ventanaIngresarDron(self):
        resultado = simpledialog.askstring("EntradaDatos", "                Ingrese el nombre del Dron:                ")
        if resultado:
            print("Dron ingresado:", resultado)
        else:
            print("Ningún Dron ingresado.")
    
    # Función para mostrar un mensaje de información
    def mostrar_infoReinicio(self):
        messagebox.showinfo("Información", "Sistema Reiniciado con Exito")

    def mostrar_infoIngresoArchivo(self):
        messagebox.showinfo("Información", "Archivo Ingresado con Exito")

app = Ventana()
app.mainloop()