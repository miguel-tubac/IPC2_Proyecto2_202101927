import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Para poder insertar el pdf a la ventana
# Para trabajar con el pdf
from tkinter import filedialog, Canvas, Scrollbar
import fitz

from LecturaXML import ConfigParser
from ListaDoble import ListaDoble
from Drones import Drones
from Grafica import*

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
    def activarTextArea(self):
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def desactivarTextArea(self):
        self.text.pack_forget()

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

           # Variable para almacenar la referencia al submenú
        self.sub_menu_var = None

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

        self.menu.add_command(label="e. ListaDrones(Grafica)", command=self.verGraficamenteLestadoSistemaDrones)

        self.menu.add_cascade(label="f. Gestion(Mensajes) ▼", menu=self.filemenu2)
        self.filemenu2.add_command(label="a. Listado(Mensajes)", command=self.listadoMensajes)
        self.filemenu2.add_separator()
        # Estos incisos se agregan en la parte inferior ya que son dinamicos:
        # self.filemenu2.add_command(label="i. Seleccionar(Mensaje) ")
        # self.filemenu2.add_command(label="ii. Mostrar(sistema)")
        # self.filemenu2.add_command(label="iii. Grafica(Instruciones)")

        self.menu.add_command(label="g. Ayuda")

        # # Crear barras de desplazamiento
        # self.scrollbar_x = Scrollbar(self, orient=tk.HORIZONTAL)
        # self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        # self.scrollbar_y = Scrollbar(self, orient=tk.VERTICAL)
        # self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # # Contenedor para el área de texto y el lienzo
        # container = tk.Frame(self)
        # container.pack(fill=tk.BOTH, expand=True)

        # # Agregar un lienzo para mostrar el PDF
        # self.canvas = Canvas(container, width=550, height=550, xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)
        # self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # # Configurar las barras de desplazamiento para que se muevan con el lienzo
        # self.scrollbar_x.config(command=self.canvas.xview)
        # self.scrollbar_y.config(command=self.canvas.yview)

        # # Crear el área de texto en el contenedor
        # self.scroll = ScrollText(container)
        # self.scroll.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


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
        self.scroll.activarTextArea()
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
            self.crearSubMenuMensajes()

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
        self.lista_mensajes = None
        self.lista_sistemas_drones = None
        # Inicializamos la variable que hace que se unan las dos listas enlazadas
        self.datosConcatenados = False
        # Esto es para borar los datos del texArea
        self.mostrarDronesEnOrdenAlfabetico()
        # Esto es para que se inicie de cero el almacenamiento de datos
        self.candtidadDeClicks = 0
        #Quita el area de texto
        self.scroll.desactivarTextArea()
        # Para reiniciar las opciones de selecion de mesajes
        self.crearSubMenuMensajes()
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
        resultado1 = simpledialog.askstring("EntradaDatos", "                Ingrese el nombre del Dron:                ")
        # Validaciones de ingreso de datos
        if resultado1:
            # Esto es para borrar y dejar limpia el text area 
            self.scroll.delete(1.0,tk.END)
            # Se instancia al dron dentro de la clase Dron() para obtener las caracteristicas
            resultado = Drones(resultado1)
            # Se unene las listas con el nuevo dron:
            listaUnida =  self.agregarDron(lista1=self.lista_drones1, lista2=resultado)
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
            print("Ningún Dron ingresado.")

    def agregarDron(self, lista1, lista2):
        nueva_lista = ListaDoble()
        # Recorre la primera lista y agrega sus elementos a la nueva lista
        for nodo in lista1.recorrer():
            nueva_lista.insertar(nodo.dato)
        # Recorre la segunda lista y agrega sus elementos a la nueva lista
        nueva_lista.insertar(lista2)
        return nueva_lista
    
    def verGraficamenteLestadoSistemaDrones(self):
        # Se recorre la lista doble de sistemas de drones
        for sistema in self.lista_sistemas_drones.recorrer():
            # Se agrega la raiz del Arbol
            raiz = arbol.agregarNodo(f"Sistema: \\n{str(sistema.dato.nombre)}")
            # Se agrega un nodo
            nodoA =  arbol.agregarNodo("Altura (mts)")
            # Se agrega a la grafica
            arbol.agregarArista(raiz, nodoA)
            #Este contador me ayuda a controlar el numero de veces que se repite el codigo
            aux = 0               
            for contenido in sistema.dato.contenido.recorrer():
                #Se agregan los drones
                nodoB = arbol.agregarNodo(contenido.dato.dron)
                arbol.agregarArista(raiz, nodoB)
                #Se agregan las letras 
                for altura in contenido.dato.alturas.recorrer():
                    if aux == 0:
                        nodoD = arbol.agregarNodo(altura.dato.letra)
                        arbol.agregarArista(nodoB, nodoD)
                        aux +=1
                    else:
                        nodoE = arbol.obtenerUltimoNodo()
                        nodoF = arbol.agregarNodo(altura.dato.letra)
                        arbol.agregarArista(nodoE, nodoF)
                # Se agregan las Alturas (mts) y como solo se necesita una vez, por eso la condicion
                if aux == 1:
                    for altura in contenido.dato.alturas.recorrer():
                        if aux == 1:
                            nodoC = arbol.agregarNodo(altura.dato.valor)
                            arbol.agregarArista(nodoA, nodoC)
                            aux +=1
                        elif int(altura.dato.valor) > 1:
                            nodoA = arbol.obtenerUltimoNodo()
                            nodoH = arbol.agregarNodo(altura.dato.valor)
                            arbol.agregarArista(nodoA, nodoH)
                        else:
                            nodoA = arbol.obtenerUltimoNodo()
                            nodoH = arbol.agregarNodo(altura.dato.valor)
                            arbol.agregarArista(nodoA, nodoH)
                            # Se detiene cuando los metros ya son menor a cero
                            break
        # Aca se geenra la grafica 
        arbol.generarGrafica()
    
    def listadoMensajes(self):
        # Esto es para borrar y dejar limpia el text area 
        self.scroll.delete(1.0,tk.END)

        mostrar ="---------------Lista de Mensajes:---------------\n"
        self.lista_mensajes.ordenar_alfabeticamenteListaMensajes()
        for mensaje in self.lista_mensajes.recorrer():
            mostrar += "nombre: "+ mensaje.dato.nombre + "\n sistemaDrones: "+ mensaje.dato.sistemaDrones + "\n"
            for instruc in mensaje.dato.instrucciones.recorrer():
                mostrar += "instruccion - dron: "+ instruc.dato.dron + " Instrucion: " + instruc.dato.valorInstrucion + "\n"
        
        # Muestra el texto en el area de texto
        self.scroll.insert(tk.END, mostrar)
         
    # Esta funcion crea los sub menus de los mensajes 
    def crearSubMenuMensajes(self):
        if self.lista_mensajes is not None:
            # Crear un nuevo menú para las opciones de mensajes
            sub_menu_mensajes = Menu(self.filemenu2)

            # Iterar sobre los mensajes y agregar opciones al submenú
            for mensaje in self.lista_mensajes.recorrer():
                sub_menu_mensajes.add_command(label=mensaje.dato.nombre, command=lambda msg=mensaje: self.seleccionar_mensaje(msg))

            # Almacenar la referencia al submenú
            self.sub_menu_var = sub_menu_mensajes

            # Agregar el submenú al menú principal
            self.filemenu2.add_cascade(label="i. Y ii Seleccionar(Mensaje)", menu=sub_menu_mensajes)
            # Esta opción se ejecutará al seleccionar uno de los mensajes
            # self.filemenu2.add_command(label="ii. Mostrar(sistema)")
            self.filemenu2.add_command(label="iii. Grafica(Instruciones)")
        else:
            #print("Sistema reiniciado")
            self.eliminarSubMenuMensajes()

    def eliminarSubMenuMensajes(self):
        if self.sub_menu_var is not None:
            # Iterar sobre los elementos del submenú y eliminar cada uno
            for item in self.sub_menu_var.winfo_children():
                self.sub_menu_var.delete(item)

            # Eliminar el submenú del menú principal
            self.filemenu2.delete("i. Y ii Seleccionar(Mensaje)")
            self.filemenu2.delete("iii. Grafica(Instruciones)")
        else:
            print("No hay submenú para eliminar")
            

    def seleccionar_mensaje(self, mensajenombre):
        # Lógica para manejar la selección del mensaje (Se mostrara: Nombre, mensaje y tiempo optimo)
        #print(f"Mensaje seleccionado: {mensajenombre.dato.nombre}")
        # Esto es para borrar y dejar limpia el text area 
        self.scroll.delete(1.0,tk.END)

        mostrar ="---------------Opcion Seleccionada i y ii:---------------\n"
        #self.lista_mensajes.ordenar_alfabeticamenteListaMensajes()
        for mensaje in self.lista_mensajes.recorrer():
            if mensajenombre.dato.nombre == mensaje.dato.nombre:
                mostrar += "nombre: "+ mensaje.dato.nombre + "\n sistemaDrones: "+ mensaje.dato.sistemaDrones + "\n"
                for instruc in mensaje.dato.instrucciones.recorrer():
                    # aqui desarrollar la logica de subir, bajar, esperar y Emitir luz
                    mostrar += "instruccion - dron: "+ instruc.dato.dron + " Instrucion: " + instruc.dato.valorInstrucion + "\n"
        
        # Muestra el texto en el area de texto
        self.scroll.insert(tk.END, mostrar)

    # def insertarPDF(self):
    #     file_path = "Graficas/ListadoDeSistema.pdf"
    #     if file_path:
    #         # Abrir el archivo PDF
    #         pdf_document = fitz.open(file_path)

    #         # Obtener el número total de páginas del PDF
    #         total_pages = pdf_document.page_count

    #         # Obtener la primera página del PDF (página 0)
    #         first_page = pdf_document.load_page(0)

    #         # Obtener las dimensiones de la página
    #         page_width = first_page.rect.width
    #         page_height = first_page.rect.height

    #         # Configurar el lienzo para que coincida con las dimensiones de la página
    #         self.canvas.config(scrollregion=(0, 0, page_width, page_height), width=page_width, height=page_height)

    #         # Convertir la página PDF a una imagen y mostrarla en el lienzo
    #         image = first_page.get_pixmap()
    #         self.image_reference = tk.PhotoImage(data=image.tobytes())
    #         self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_reference)

    #         # Cerrar el archivo PDF después de usarlo
    #         pdf_document.close()
        

    # Función para mostrar un mensaje de información
    def mostrar_infoReinicio(self):
        messagebox.showinfo("Información", "Sistema Reiniciado con Exito")

    def mostrar_infoIngresoArchivo(self):
        messagebox.showinfo("Información", "Archivo Ingresado con Exito")

app = Ventana()
app.mainloop()