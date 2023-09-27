import xml.etree.ElementTree as ET
from ListaDoble import ListaDoble
from Drones import Drones
from Contenido import Contenido
from SistemaDrones import SistemaDrones
from Alturas import Alturas
from Instruciones import Instruciones
from Mensajes import Mensajes

class ConfigParser:
    def __init__(self, xml_file_path):
        self.xml_file_path = xml_file_path
        self.tree = ET.parse(xml_file_path)
        self.root = self.tree.getroot()

    def get_lista_drones(self):
        # Creo la instancia de la listaDoble
        drones = ListaDoble() 
        lista_drones = self.root.find('listaDrones')
        # Recorro cada elemento que contenga 'dron'
        for dron_element in lista_drones.findall('dron'):
            #Creo una instancia de mi clase drones, para posterior acceder a sus datos
            ndron = Drones(dron_element.text) 
            # Inserto la instancia de la clase que declare ndron
            drones.insertar(ndron)
        # Devuelvo la instancai de la lista doble para poder recorrela 
        return drones

    def get_lista_sistemas_drones(self):
        #Declaro mi listadoble en donde se almacenaran 2 listas dobles
        sistemas_drones = ListaDoble()
        lista_sistemas_drones = self.root.find('listaSistemasDrones')
        #se recorre en cada elemento del xml para encontrar 'sistemaDrones'
        for sistema_drones_element in lista_sistemas_drones.findall('sistemaDrones'):
            # se obtinene los datos del xml
            nombre = sistema_drones_element.get('nombre')
            altura_maxima = sistema_drones_element.find('alturaMaxima').text
            cantidad_drones = sistema_drones_element.find('cantidadDrones').text
            # se cra otra instancia de la listadoble en donde se almacenara el dron y la otra listadoble datosAltura
            contenido = ListaDoble()
            # recorremos el xml por cada 'contenido'
            for contenido_element in sistema_drones_element.findall('contenido'):
                # se almacena el nombre del dron
                dron = contenido_element.find('dron').text
                # se cra otra instancia de la listadoble en donde se almacenara las alturas y letras
                datosAltura = ListaDoble()
                # Recorro el xml en busca de 'alturas'
                for altura in contenido_element.find('alturas'):
                    # obtengo el valor 
                    alturas = altura.get("valor")
                    # obtengo la letra que acompana el valor
                    letras = altura.text
                    # Creo una instancia de la clase Alturas
                    ingresoAlturas = Alturas(alturas, letras)
                    # Almaceno la instancia en la listadoble de datosAltura
                    datosAltura.insertar(ingresoAlturas)
                # Creo una instancia de la clase Contenido y en la misma meto una listadoble datosAltura    
                datoDeDron = Contenido(dron, datosAltura)
                # La ingreso a la listadoble contenido
                contenido.insertar(datoDeDron)
            # Creo una instancia de la clase SistemaDrones, en donde almaceno una listadoble contenido
            datoDeSistemaDron = SistemaDrones(nombre, altura_maxima, cantidad_drones, contenido)
            # Inserto la instancia en la lista doble sistemas_drones
            sistemas_drones.insertar(datoDeSistemaDron)
        # Devuelvo el sistemas_drones para poder reccorer en la misma
        return sistemas_drones

    def get_lista_mensajes(self):
        # Declaro mi listadoble para almacenar los mensajes
        mensajes = ListaDoble()
        lista_mensajes = self.root.find('listaMensajes')
        # Recorro por cada iteracion de 'Mensaje'
        for mensaje_element in lista_mensajes.findall('Mensaje'):
            # Obtengo los datos del xml y los almaceno en vaiables
            nombre = mensaje_element.get('nombre')
            sistema_drones = mensaje_element.find('sistemaDrones').text
            # Declaro otra instancia de la listadoble para almacenar las instrucciones
            instrucciones = ListaDoble()
            # Recorro el xml por cada 'instrucciones'
            for instruccion_element in mensaje_element.find('instrucciones').findall('instruccion'):
                # Se obtine el nombre del dron
                dron = instruccion_element.get('dron')
                # Se obtine la instrucion o los valores de movimiento del dron
                valor = instruccion_element.text
                # Instancia de la clase Instruciones
                instrucionesDeclaracion = Instruciones(dron, valor)
                # Se ingresa la clase a la lista doblemente enlazada 
                instrucciones.insertar(instrucionesDeclaracion)
            # Instancia de la clase Mensaje que se le psan los parametros
            instanciaMensaje = Mensajes(nombre, sistema_drones, instrucciones)
            # Se almacena la informacion en la istadoble
            mensajes.insertar(instanciaMensaje)
        # Se retorna la listaDoble mensaje para poder recorrerlo 
        return mensajes

# Uso de la clase ConfigParser
if __name__ == "__main__":
    xml_file_path = "EntradaIPC2.xml"  # Reemplaza con la ruta de tu archivo XML
    parser = ConfigParser(xml_file_path)


    lista_drones = parser.get_lista_drones()
    lista_drones.ordenar_alfabeticamente()
    print("--------------------------------------")
    print("           Drones:    ")
    for elemento in lista_drones.recorrer():
        print(elemento.dato.nombre)
    print("--------------------------------------\n")
    

    lista_sistemas_drones = parser.get_lista_sistemas_drones()
    print("     Lista de Sistemas de Drones:  ")
    for sistema in lista_sistemas_drones.recorrer():
        print("nombre: ",sistema.dato.nombre,
              "\naltura_maxima :",sistema.dato.alturaMaxima,
              "\ncantidad_drones: ",sistema.dato.cantidadDrones
              )
        for contenido in sistema.dato.contenido.recorrer():
            print("dron: ", contenido.dato.dron)
            for altura in contenido.dato.alturas.recorrer():
                print("altura - valor= ", altura.dato.valor, " Letra: ", altura.dato.letra)
    print("--------------------------------------\n")
   
    lista_mensajes = parser.get_lista_mensajes()
    print("     Lista de Mensajes:  ")
    for mensaje in lista_mensajes.recorrer():
        print("nombre: ",mensaje.dato.nombre,
              "\nsistemaDrones: ", mensaje.dato.sistemaDrones)
        for instruc in mensaje.dato.instrucciones.recorrer():
            print("instruccion - dron: ", instruc.dato.dron," Instrucion: ",instruc.dato.valorInstrucion)

    lista_drones.borrar_todos()
    #lista_drones = parser.get_lista_drones() # Este se tine que quitar
    print("--------------------------------------")
    print("           Drones:    ")
    for elemento in lista_drones.recorrer():
        print(elemento.dato.nombre)
    print("--------------------------------------\n")
