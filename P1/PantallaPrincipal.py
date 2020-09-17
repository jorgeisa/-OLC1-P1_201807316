import os
from tkinter import *  # ventana
from tkinter import Menu  # barra de tareas
from tkinter import filedialog  # filechooser
from tkinter import scrolledtext  # textarea
from tkinter import messagebox  # message box
from AnalizadorLexicoJS import AnalizadorLexicoJS
from AnalizadorLexicoCSS import AnalizadorLexicoCSS
from AnalizadorHTML import AnalizadorHTML
from PIL import Image
from Token import TipoToken
from Token import TipoTokenCSS
from Token import TipoTokenHTML


class PantallaPrincipal:
    nameArchivoEntrada = ""
    contadorReportesHtml = 0
    contadorReprotesErrores = 0
    contadorImagenesLabel = 1
    booleanAnalizar = False
    booleanAbrirImagen = False

    # Metodo que contiene la definicion de la interfaz grafica
    def getInfo(self, event):
        string = self.txtEntrada.index(INSERT)
        print(string)
        self.lblPosition.destroy()
        self.lblPosition = Label(self.window, text=f"Posicion (V, H): {string}")
        self.lblPosition.place(x=200, y=465)

    def __init__(self):
        self.ultimoPathAbierto = ""
        self.ultimaExtensionAbierta = ""
        self.window = Tk()
        self.txtEntrada = Entry(self.window, width=15)
        self.txtConsola = Entry(self.window, width=15)
        # self.fondo = Label(self.window)

        self.txtBitacoraCSS = Entry(self.window, width=15)

        # PROPIEDADES DE LA VENTANA, CENTRADO, TAMANIO, etc
        self.window.title("Proyecto 1 - Analizador JavaScript")  # Titulo de la ventana
        widthTK = 800  # Ancho predeterminado de la ventana
        heightTK = 700  # Alura predeterminada de la ventana
        widthScreen = self.window.winfo_screenwidth()  # Ancho de la pantalla
        heightScreen = self.window.winfo_screenheight()  # Altura de la pantalla

        x = (widthScreen / 2) - (widthTK / 2)  # Posicion de centrado en x
        y = (heightScreen / 2) - (heightTK / 2)  # Posicion de centrado en y

        self.window.geometry(
            '%dx%d+%d+%d' % (widthTK + 550, heightTK, x - 280, y - 25))  # Colocarle la vetana en el centro

        self.window.configure(bg='#6A90FF')  # Darle color a la ventana (fondo)

        # LABEL TITULO PROPIEDADES
        # Posicionandolo en la ventana, texto a mostrar, tipo letra, fondo del label
        self.lbl = Label(self.window, text="Proyecto 1 - Pantalla Principal", font=("Arial Bold", 15), bg='#17A589')
        self.lbl.pack(fill=X)  # Label estirado por el eje X en su posicion

        # PROPIEDADES DEL MENU DESPLEGABLE
        # Agregando las opciones en el menu desplegable
        self.menu = Menu(self.window)
        self.file_item = Menu(self.menu)  # File
        self.file_item.add_command(label='Nuevo', command=self.nuevoOpcionMenu)
        self.file_item.add_separator()
        self.file_item.add_command(label='Abrir Archivo', command=self.abrirArchivo)
        self.file_item.add_separator()
        self.file_item.add_command(label='Guardar Archivo', command=self.guardarEnRutaArchivo)
        self.file_item.add_separator()
        self.file_item.add_command(label='Guardar archivo como...', command=self.guardarArchivoComo)
        self.file_item.add_separator()
        self.file_item.add_command(label='Ejecutar Analisis JS', command=self.Analisis)
        self.file_item.add_separator()
        self.file_item.add_command(label='Exit', command=exit)

        self.report_item = Menu(self.menu)  # Reports
        # self.report_item.add_separator()
        # self.report_item.add_command(label='Errores!', command=self.reportarErrores)
        self.report_item.add_separator()
        self.report_item.add_command(label='Tree')

        # Agregando estilo de menu - cascada
        self.menu.add_cascade(label='Menu Archivo', menu=self.file_item)
        self.menu.add_cascade(label='Reportes', menu=self.report_item)

        # COLOCANDO EL MENU CON OPCIONES DENTRO DEL WINDOW
        self.window.config(menu=self.menu)

        # PROPIEDADES DEL TXTENTRADA (TEXTO A ANALIZAR)
        self.txtEntrada = scrolledtext.ScrolledText(self.window, width=110, height=25)  # 80,25
        self.txtEntrada.pack()
        self.txtEntrada.place(x=50, y=50)

        # PROPIEDADES DEL TXT BITACORA
        self.txtBitacoraCSS = scrolledtext.ScrolledText(self.window, width=65, height=12, bg="#000000",
                                                        fg="white")  # 80,25
        self.txtBitacoraCSS.pack()
        self.txtBitacoraCSS.place(x=975, y=490)
        self.lblBitacoraCSS = Label(self.window, text=f"BITACORA CSS: ")
        self.lblBitacoraCSS.place(x=975, y=465)

        # LABEL PARA MOSTRAR IMAGENES DE GRAFO
        self.lbltxtGrafica = Label(self.window, text=f"Graficas JS:")
        self.lbltxtGrafica.place(x=975, y=420)

        self.mostrarImagenes = Button(self.window, text="Mostrar Imagen", bg="black", fg="white",
                                      command=self.colocarImagenesEnLabel)
        self.mostrarImagenes.place(x=1070, y=420)

        self.img = PhotoImage()
        self.fondo = Label()
        self.imgAbrir = Image

        #  colores
        self.txtEntrada.tag_config('colorReservada', foreground='red')
        self.txtEntrada.tag_config('colorVariable', foreground='green')  # ID?
        self.txtEntrada.tag_config('colorCadenas', foreground='yellow')  # String y Char
        self.txtEntrada.tag_config('colorNumBool', foreground='blue')  # Int y Bool  numeros y booleans?
        self.txtEntrada.tag_config('colorComentario', foreground='gray')  #
        self.txtEntrada.tag_config('colorOperadores', foreground='orange')  #
        self.txtEntrada.tag_config('colorOtros', foreground='black')  #

        # PROPIEDADES DE LA CONSOLA, SALIDA (ANALISIS EXISTOSO, etc)
        self.lbl = Label(self.window, text="Console:")
        self.lbl.place(x=50, y=465)
        self.txtConsola = scrolledtext.ScrolledText(self.window, width=110, height=12, bg="#000000", fg="white")
        self.txtConsola.place(x=50, y=490)
        self.btn = Button(self.window, text="Analizar JS, CSS, HTML ", bg="black", fg="white",
                          command=self.Analisis)  # boton ANALYZE

        self.btn.place(x=655, y=460)
        # self.btn = Button(self.window, text="Analyze CSS", bg="black", fg="white", command="")  # boton ANALYZE
        # self.btn.place(x=755, y=460)
        # self.btn = Button(self.window, text="Analyze HTML", bg="black", fg="white",
        #                   command=self.getInfo)  # boton ANALYZE
        # self.btn.place(x=855, y=460)

        self.txtEntrada.bind("<Button-1>", self.getInfo)
        self.txtEntrada.bind("<Button-2>", self.getInfo)
        self.txtEntrada.bind("<Button-3>", self.getInfo)

        self.lblPosition = Label(self.window, text=f"Posicion (V, H): --")
        self.lblPosition.place(x=200, y=465)

        # Dispara la interfaz y la mantiene abierta
        self.window.mainloop()

    def Analisis(self):
        # Si abrimos algun archivo
        if self.nameArchivoEntrada != "":
            print(f"RUTA DE ENTRADA: {self.nameArchivoEntrada}")

            # Recuperar Extension del archivo abierto
            extension = os.path.splitext(self.nameArchivoEntrada)[1]
            print(f"{extension} es la extension\n\n")

            # El texto de entrada
            entrada = self.txtEntrada.get("1.0", END)  # fila 1 col 0 hasta fila 2 col 10

            # Si la extension es .js
            if extension == ".js":
                self.booleanAnalizar = True
                miScanner = AnalizadorLexicoJS()
                listaTokens = miScanner.ScannerJS(entrada)

                if not os.path.exists(miScanner.pathSalida):
                    print("Direccion no existe! Se creo :D")
                    os.makedirs(miScanner.pathSalida)

                # Borrar la consola
                self.txtConsola.delete("1.0", END)

                # Imprimir en interfaz la lista de Tokens y de Errores
                self.imprimirListasEnConsola(miScanner)
                messagebox.showinfo('Project 1', 'Analisis Finalizado JS!')
                print(f"Este es la direccion de salida: {miScanner.pathSalida}")

                self.contadorReprotesErrores += 1
                pathReporteError = f"{miScanner.pathSalida}JS_ReporteCorregido{self.contadorReprotesErrores}.js"
                self.crearArchivo(pathReporteError, miScanner.textoCorregido)

                self.colorearJS(miScanner)
                self.ultimoPathAbierto = miScanner.pathSalida

                self.reportarErrores(miScanner, "JS")

                self.booleanAbrirImagen = True

            elif extension == ".css":
                self.booleanAnalizar = True
                miScanner = AnalizadorLexicoCSS()
                listaTokens = miScanner.ScannerCSS(entrada)

                if not os.path.exists(miScanner.pathSalida):
                    print("Direccion no existe! Se creo :D")
                    os.makedirs(miScanner.pathSalida)

                # Borrar la consola
                self.txtConsola.delete("1.0", END)

                self.imprimirListasEnConsola(miScanner)
                messagebox.showinfo('Project 1', 'Analisis Finalizado CSS!')
                print(f"Este es la direccion de salida: {miScanner.pathSalida}")

                self.contadorReprotesErrores += 1
                pathReporteError = f"{miScanner.pathSalida}CSS_ReporteCorregido{self.contadorReprotesErrores}.css"
                self.crearArchivo(pathReporteError, miScanner.textoCorregido)

                self.colorearCSS(miScanner)
                bitacora = miScanner.bitacoraCSS
                self.txtBitacoraCSS.delete("1.0", END)
                self.txtBitacoraCSS.insert(END, f"{bitacora}")

                self.ultimoPathAbierto = miScanner.pathSalida
                self.reportarErrores(miScanner, "CSS")

            elif extension == ".html":
                self.booleanAnalizar = True
                miScanner = AnalizadorHTML()
                listaTokens = miScanner.ScannerHTML(entrada)

                if not os.path.exists(miScanner.pathSalida):
                    print("Direccion no existe! Se creo :D")
                    os.makedirs(miScanner.pathSalida)

                self.txtConsola.delete("1.0", END)

                self.imprimirListasEnConsola(miScanner)
                messagebox.showinfo('Project 1', 'Analisis Finalizado HTML!')
                print(f"Este es la direccion de salida: {miScanner.pathSalida}")

                self.contadorReprotesErrores += 1
                pathReporteError = f"{miScanner.pathSalida}HTML_ReporteCorregido{self.contadorReprotesErrores}.html"
                self.crearArchivo(pathReporteError, miScanner.textoCorregido)

                self.colorearHTML(miScanner)
                self.ultimoPathAbierto = miScanner.pathSalida
                self.reportarErrores(miScanner, "HTML")

        else:
            self.txtConsola.delete("1.0", END)
            self.txtConsola.insert("1.0", "Abra un archivo de entrada!")
            # 111@11^11&11~

    # ------------------------------- COLORES ANALIZAR JS ------------------------------------------------------------
    def colorearJS(self, miScannerJS):
        # imprimir Tokens en consola
        self.txtEntrada.delete("1.0", END)
        for i in miScannerJS.lista_Tokens:
            self.evaluarJS(i)

    def evaluarJS(self, token):
        if token.tipoToken.value == 1 or token.tipoToken.value == 2 or token.tipoToken.value == 3 or \
                token.tipoToken.value == 4 or token.tipoToken.value == 5 or token.tipoToken.value == 6 or \
                token.tipoToken.value == 7 or token.tipoToken.value == 8 or token.tipoToken.value == 9 or \
                token.tipoToken.value == 10 or token.tipoToken.value == 11 or token.tipoToken.value == 12 or \
                token.tipoToken.value == 13 or token.tipoToken.value == 14 or token.tipoToken.value == 15 or \
                token.tipoToken.value == 16 or token.tipoToken.value == 17 or token.tipoToken.value == 18 or \
                token.tipoToken.value == 19:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorReservada')

        elif token.tipoToken.value == 300:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorVariable')
        elif token.tipoToken.value == 304 or token.tipoToken.value == 305:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorCadenas')
        elif token.tipoToken.value == 301 or token.tipoToken.value == 100 or token.tipoToken.value == 101 \
                or token.tipoToken.value == 102 or token.tipoToken.value == 110 or token.tipoToken.value == 112 \
                or token.tipoToken.value == 113 or token.tipoToken.value == 114 or token.tipoToken.value == 115 \
                or token.tipoToken.value == 118 or token.tipoToken.value == 121 or token.tipoToken.value == 122:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorNumBool')
        elif token.tipoToken.value == 302 or token.tipoToken.value == 303:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorComentario')
        elif token.tipoToken.value == 116 or token.tipoToken.value == 117 or token.tipoToken.value == 120 \
                or token.tipoToken.value == 200 or token.tipoToken.value == 201 or token.tipoToken.value == 202 \
                or token.tipoToken.value == 203:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorOperadores')
        elif token.tipoToken.value == 351:
            self.txtEntrada.insert(END, f"{token.lexemaValor}")
        elif token.tipoToken.value != 351:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorOtros')

    # ------------------------------- COLORES ANALIZAR CSS ------------------------------------------------------------
    def colorearCSS(self, miScannerCSS):
        self.txtEntrada.delete("1.0", END)
        for i in miScannerCSS.lista_Tokens:
            self.evaluarCSS(i)

    def evaluarCSS(self, token):
        if token.tipoToken.value == 1 or token.tipoToken.value == 2:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorReservada')
        elif token.tipoToken.value == 301:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorVariable')
        elif token.tipoToken.value == 302:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorCadenas')
        elif token.tipoToken.value == 303:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorNumBool')
        elif token.tipoToken.value == 300:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorComentario')
        elif token.tipoToken.value == 200 or token.tipoToken.value == 201 or token.tipoToken.value == 110:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorOperadores')
        elif token.tipoToken.value == 401:
            self.txtEntrada.insert(END, f"{token.lexemaValor}")
        elif token.tipoToken.value != 401:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorOtros')

    # --------------------------- Colorear HTML  -------------------------------
    def colorearHTML(self, miScannerHTML):
        self.txtEntrada.delete("1.0", END)
        for i in miScannerHTML.lista_Tokens:
            self.evaluarHTML(i)

    def evaluarHTML(self, token):
        if token.tipoToken.value == 100:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorReservada')
        elif token.tipoToken.value == 400:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorVariable')
        elif token.tipoToken.value == 403:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorCadenas')
        elif token.tipoToken.value == 3:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorNumBool')
        elif token.tipoToken.value == 402:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorComentario')
        elif token.tipoToken.value == 1 or token.tipoToken.value == 2:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorOperadores')
        elif token.tipoToken.value == 401 or token.tipoToken.value == 500:
            self.txtEntrada.insert(END, f"{token.lexemaValor}")
        elif token.tipoToken.value != 500 or token.tipoToken.value == 401:
            self.txtEntrada.insert(END, f"{token.lexemaValor}", 'colorOtros')

    # Dispara el Filechooser
    def abrirArchivo(self):
        nameFile = filedialog.askopenfilename(title="Seleccione archivo", filetypes=
        (("js files", "*.js"), ("html files", "*.html"), ("css files", "*.css"), ("All Files", "*.*")))
        if nameFile != '':
            self.nameArchivoEntrada = nameFile
            archi1 = open(nameFile, "r", encoding="utf-8")  # Lectura del archivo
            contenido = archi1.read()  # Obteniendo el texto / contenido
            archi1.close()  # Cerrando archivo
            self.txtEntrada.delete("1.0", END)
            self.txtEntrada.insert("1.0", contenido)

    def nuevoOpcionMenu(self):
        self.txtEntrada.delete("1.0", END)  # limpio entrada de texto
        self.txtConsola.delete("1.0", END)  # limpio consola
        self.ultimoPathAbierto = ""  # limpio el path guardado
        self.ScannerGlobal = ""
        self.booleanAnalizar = False

    def guardarEnRutaArchivo(self):
        if self.ultimoPathAbierto != "":
            entradaTexto = self.txtEntrada.get("1.0", END)
            self.crearArchivo(self.ultimoPathAbierto, entradaTexto)
        else:
            print("No hay path aun!... >:[")

    # Para colocarle un nombre y extension al archivo que quiero guardar
    def guardarArchivoComo(self):
        nameFile = filedialog.asksaveasfilename(title="Seleccione archivo", defaultextension='.js',
                                                filetypes=[("js files", '*.js'), ("html files", '*.html'),
                                                           ("css files", '*.css'), ("txt files", '*.txt')])
        if nameFile != '':
            extension = os.path.splitext(nameFile)[1]
            print(f"Su archivo tiene extension: {extension}")
            entradaTexto = self.txtEntrada.get("1.0", END)
            self.crearArchivo(nameFile, entradaTexto)
        else:
            print("No se escogio o se cancelo!.")

    # Crear un archivo de extension en el nombre
    def crearArchivo(self, path, textoCorregido):
        # C:/Users/Isaac/Desktop/nombrexd.txt
        # PATHL: C:\Users\Isaac\Desktop\Destino Prueba\CorregidoHtml.html
        file = open(f"{path}", "w")
        file.write(f"{textoCorregido}")
        file.close()

    # LAS LISTAS DE TODOS LOS ANALIZADORES SE LLAMAN IGUAL, ASI SOLO LLAMO A ESTA FUNCION
    def imprimirListasEnConsola(self, miScannerP):
        # Contadores de Listas
        contadorT = 0
        contadorE = 0

        # imprimir Errores en la consola
        for i in miScannerP.lista_ErroresLexicos:
            contadorE += 1
            self.txtConsola.insert(END, f"{contadorE}. ERROR LEXICO: {i.valor}, "
                                        f"POSICION (H,V): {i.posicion.getPosicionH()} ,"
                                        f"{i.posicion.getPosicionV()}\n")

        self.txtConsola.insert(END, "\n-------------------------------------------------------------\n\n")

        # imprimir Tokens en consola
        for i in miScannerP.lista_Tokens:
            if i.tipoToken.name != "NINGUNO":
                contadorT += 1
                self.txtConsola.insert(END, f"{contadorT}. TOKEN: {i.tipoToken.name} ,"
                                            f" VALOR: {i.lexemaValor}\n")

    def reportarErrores(self, miScannerP, lenguaje):
        # PATHL: C:\Users\Isaac\Desktop\VidaMRR-Curso-CSS-master\Tabla\ReporteHTML
        # C:\Users\Isaac\Desktop\Destino Prueba\ReportesHTML
        self.contadorReportesHtml += 1
        path = f"C:/Users/Isaac/Desktop/Destino Prueba" \
               f"/ReportesHTML/ReporteError{lenguaje}{self.contadorReportesHtml}.html"

        file = open(f"{path}", "w")
        if self.booleanAnalizar:
            # Escribir el inicio del HTML
            file.write(f"<!DOCTYPE html>\n"
                       f"<html lang = \"en\">\n"
                       f"<head>\n"
                       f"<meta charset = \"UTF-8\">\n"
                       f"<title> Proyecto 1 OLC1 - 201807316 </title>\n"
                       f"<link rel = \"stylesheet\" href = \"tabla.css\">\n"
                       f"</head>\n"
                       f"<body>\n"
                       f"<div id= \"main-container\">\n"
                       f"<table>\n"
                       f"<thead>\n"
                       f"<tr>\n"
                       f"<th>No.</th><th>Linea</th><th>Columna</th><th>Descripcion</th>\n"
                       f"</tr>\n"
                       f"</thead>\n")

            contadorE = 0
            for i in miScannerP.lista_ErroresLexicos:
                contadorE += 1
                file.write(f"<tr>\n"
                           f"<td>{contadorE}</td><td>{i.posicion.getPosicionV()}</td>"
                           f"<td>{i.posicion.getPosicionH()}</td>"
                           f"<td>El valor de error lexico es: {i.valor}</td>")

            # Escribir la parte final
            file.write(f"</table>\n"
                       f"</div>\n"
                       f"</body>\n"
                       f"</html>\n")
        file.close()

    def colocarImagenesEnLabel(self):
        if self.booleanAbrirImagen == True:
            if self.contadorImagenesLabel < 4:
                self.img = PhotoImage(file=f"AFD {self.contadorImagenesLabel}.png")
                self.fondo = Label(self.window, image=self.img, width=550, height=350)
                self.fondo.place(x=970, y=50)
                self.imgAbrir = Image.open(f"AFD {self.contadorImagenesLabel}.png")
                self.imgAbrir.show()
            else:
                self.contadorImagenesLabel = 0
            self.contadorImagenesLabel += 1
        else:
            print("No ha analizado aun!")
