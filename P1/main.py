from PantallaPrincipal import PantallaPrincipal
import os

def crearArchivo():
    # os.linesep para separar una linea de otra
    file = open("C:/Users/Isaac/Desktop/nombrexd.txt", "w")
    file.write("Primera línea\n")
    file.write("Segunda línea")
    file.close()


# crearArchivo()
iniciar = PantallaPrincipal()
