from PantallaPrincipal import PantallaPrincipal
import os

def crearArchivo():
    file = open("C:/Users/Isaac/Desktop/nombrexd.txt", "w")
    file.write("Primera línea" + os.linesep)
    file.write("Segunda línea")
    file.close()


#crearArchivo()
iniciar = PantallaPrincipal()
