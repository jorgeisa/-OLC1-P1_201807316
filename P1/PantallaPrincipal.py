import os
from tkinter import *  # ventana
from tkinter import Menu  # barra de tareas
from tkinter import filedialog  # filechooser
from tkinter import scrolledtext  # textarea
from tkinter import messagebox  # message box
from AnalizadorLexicoJS import AnalizadorLexicoJS
from AnalizadorLexicoCSS import AnalizadorLexicoCSS
from Token import TipoToken
from Token import TipoTokenCSS


class PantallaPrincipal:
    nameArchivoEntrada = ""

    # Metodo que contiene la definicion de la interfaz grafica

    def __init__(self):
        self.window = Tk()
        self.txtEntrada = Entry(self.window, width=15)
        self.txtConsola = Entry(self.window, width=15)

        # PROPIEDADES DE LA VENTANA, CENTRADO, TAMANIO, etc
        self.window.title("Proyecto 1 - Analizador JavaScript")  # Titulo de la ventana
        widthTK = 800  # Ancho predeterminado de la ventana
        heightTK = 700  # Alura predeterminada de la ventana
        widthScreen = self.window.winfo_screenwidth()  # Ancho de la pantalla
        heightScreen = self.window.winfo_screenheight()  # Altura de la pantalla

        x = (widthScreen / 2) - (widthTK / 2)  # Posicion de centrado en x
        y = (heightScreen / 2) - (heightTK / 2)  # Posicion de centrado en y

        self.window.geometry('%dx%d+%d+%d' % (widthTK + 200, heightTK, x, y - 25))  # Colocarle la vetana en el centro

        self.window.configure(bg='#6A90FF')  # Darle color a la ventana (fondo)

        # LABEL TITULO PROPIEDADES
        # Posicionandolo en la ventana, texto a mostrar, tipo letra, fondo del label
        self.lbl = Label(self.window, text="Proyecto 1 - Pantalla Principal", font=("Arial Bold", 15), bg='#17A589')
        self.lbl.pack(fill=X)  # Label estirado por el eje X en su posicion

        # PROPIEDADES DEL MENU DESPLEGABLE
        # Agregando las opciones en el menu desplegable
        self.menu = Menu(self.window)
        self.file_item = Menu(self.menu)  # File
        self.file_item.add_command(label='Nuevo')
        self.file_item.add_separator()
        self.file_item.add_command(label='Abrir Archivo', command=self.abrirArchivo)
        self.file_item.add_separator()
        self.file_item.add_command(label='Guardar Archivo')
        self.file_item.add_separator()
        self.file_item.add_command(label='Guardar archivo como...')
        self.file_item.add_separator()
        self.file_item.add_command(label='Ejecutar Analisis JS', command=self.Analisis)
        self.file_item.add_separator()
        self.file_item.add_command(label='Exit')

        self.report_item = Menu(self.menu)  # Reports
        self.report_item.add_separator()
        self.report_item.add_command(label='Errors')
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
        self.btn = Button(self.window, text="Analyze JS", bg="black", fg="white",
                          command=self.Analisis)  # boton ANALYZE
        self.btn.place(x=655, y=460)
        self.btn = Button(self.window, text="Analyze CSS", bg="black", fg="white", command="")  # boton ANALYZE
        self.btn.place(x=755, y=460)
        self.btn = Button(self.window, text="Analyze HTML", bg="black", fg="white", command="")  # boton ANALYZE
        self.btn.place(x=855, y=460)

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
                miScanner = AnalizadorLexicoJS()
                listaTokens = miScanner.ScannerJS(entrada)

                # Borrar la consola
                self.txtConsola.delete("1.0", END)

                # Imprimir en interfaz la lista de Tokens y de Errores
                self.imprimirListasEnConsola(miScanner)
                messagebox.showinfo('Project 1', 'Analisis Finalizado JS!')
                print(f"Este es la direccion de salida: {miScanner.pathSalida}")
                self.crearArchivo(f"{miScanner.pathSalida}", miScanner.textoCorregido)
                self.colorearJS(miScanner)

            elif extension == ".css":
                miScanner = AnalizadorLexicoCSS()
                listaTokens = miScanner.ScannerCSS(entrada)

                # Borrar la consola
                self.txtConsola.delete("1.0", END)

                self.imprimirListasEnConsola(miScanner)
                messagebox.showinfo('Project 1', 'Analisis Finalizado CSS!')
                print(f"Este es la direccion de salida: {miScanner.pathSalida}")
                self.crearArchivo(f"{miScanner.pathSalida}", miScanner.textoCorregido)
                self.colorearCSS(miScanner)
                print(".css")
            elif extension == ".html":
                print(".html")
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

    def crearArchivo(self, path, textoCorregido):
        # C:/Users/Isaac/Desktop/nombrexd.txt
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
