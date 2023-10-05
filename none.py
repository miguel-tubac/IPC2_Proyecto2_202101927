import tkinter as tk
from tkinter import messagebox
import os

class MiVentana:
    def __init__(self, root):
        self.root = root
        self.root.title("Ejemplo de Hipervínculo")

        label_ayuda = tk.Label(root, text="Haz clic aquí para obtener ayuda", fg="blue", cursor="hand2")
        label_ayuda.pack(pady=10)
        label_ayuda.bind("<Button-1>", self.abrir_documento)

    def abrir_documento(self, event):
        # Ruta del documento en la carpeta raíz
        ruta_documento = "nombre_del_documento.txt"  # Reemplaza con el nombre de tu documento

        # Verificar si el archivo existe antes de intentar abrirlo
        if os.path.exists(ruta_documento):
            os.startfile(ruta_documento)
        else:
            messagebox.showerror("Error", "El documento no se encuentra en la carpeta raíz.")

if __name__ == "__main__":
    root = tk.Tk()
    ventana = MiVentana(root)
    root.mainloop()
