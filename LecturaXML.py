import xml.etree.ElementTree as ET

class ConfigParser:
    def __init__(self, xml_file_path):
        self.xml_file_path = xml_file_path
        self.tree = ET.parse(xml_file_path)
        self.root = self.tree.getroot()

    def get_lista_drones(self):
        drones = []
        lista_drones = self.root.find('listaDrones')
        for dron_element in lista_drones.findall('dron'):
            drones.append(dron_element.text)
        return drones

    def get_lista_sistemas_drones(self):
        sistemas_drones = []
        lista_sistemas_drones = self.root.find('listaSistemasDrones')
        for sistema_drones_element in lista_sistemas_drones.findall('sistemaDrones'):
            nombre = sistema_drones_element.get('nombre')
            altura_maxima = sistema_drones_element.find('alturaMaxima').text
            cantidad_drones = sistema_drones_element.find('cantidadDrones').text
            contenido = []
            for contenido_element in sistema_drones_element.findall('contenido'):
                dron = contenido_element.find('dron').text
                alturas = [altura.text for altura in contenido_element.find('alturas')]
                contenido.append({'dron': dron, 'alturas': alturas})
            sistemas_drones.append({'nombre': nombre, 'altura_maxima': altura_maxima, 'cantidad_drones': cantidad_drones, 'contenido': contenido})
        return sistemas_drones

    def get_lista_mensajes(self):
        mensajes = []
        lista_mensajes = self.root.find('listaMensajes')
        for mensaje_element in lista_mensajes.findall('Mensaje'):
            nombre = mensaje_element.get('nombre')
            sistema_drones = mensaje_element.find('sistemaDrones').text
            instrucciones = []
            for instruccion_element in mensaje_element.find('instrucciones').findall('instruccion'):
                dron = instruccion_element.get('dron')
                valor = instruccion_element.text
                instrucciones.append({'dron': dron, 'valor': valor})
            mensajes.append({'nombre': nombre, 'sistema_drones': sistema_drones, 'instrucciones': instrucciones})
        return mensajes

# Uso de la clase ConfigParser
if __name__ == "__main__":
    xml_file_path = "EntradaIPC2.xml"  # Reemplaza con la ruta de tu archivo XML
    parser = ConfigParser(xml_file_path)
    
    lista_drones = parser.get_lista_drones()
    print("Lista de Drones:", lista_drones)
    
    lista_sistemas_drones = parser.get_lista_sistemas_drones()
    print("Lista de Sistemas de Drones:")
    for sistema in lista_sistemas_drones:
        print(sistema)
    
    lista_mensajes = parser.get_lista_mensajes()
    print("Lista de Mensajes:")
    for mensaje in lista_mensajes:
        print(mensaje)
