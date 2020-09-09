from tkinter import *  # ventana
from tkinter import Menu  # barra de tareas
from tkinter import filedialog  # filechooser
from tkinter import scrolledtext  # textarea
from tkinter import messagebox  # message box
from AnalizadorLexicoJS import AnalizadorLexicoJS


class PantallaPrincipal:
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

        self.window.geometry('%dx%d+%d+%d' % (widthTK+200, heightTK, x, y - 25))  # Colocarle la vetana en el centro

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
        self.file_item.add_command(label='Ejecutar Analisis JS', command=self.AnalisisJS)
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
        self.txtEntrada = scrolledtext.ScrolledText(self.window, width=110, height=25)  #  80,25
        self.txtEntrada.pack()
        self.txtEntrada.place(x=50, y=50)

        # PROPIEDADES DE LA CONSOLA, SALIDA (ANALISIS EXISTOSO, etc)
        self.lbl = Label(self.window, text="Console:")
        self.lbl.place(x=50, y=465)
        self.txtConsola = scrolledtext.ScrolledText(self.window, width=110, height=10, bg="#000000", fg="white")
        self.txtConsola.place(x=50, y=490)
        self.btn = Button(self.window, text="Analyze JS", bg="black", fg="white", command=self.AnalisisJS)  # boton ANALYZE
        self.btn.place(x=655, y=460)
        self.btn = Button(self.window, text="Analyze CSS", bg="black", fg="white", command="")  # boton ANALYZE
        self.btn.place(x=755, y=460)
        self.btn = Button(self.window, text="Analyze HTML", bg="black", fg="white", command="")  # boton ANALYZE
        self.btn.place(x=855, y=460)

        # Dispara la interfaz y la mantiene abierta
        self.window.mainloop()

    def AnalisisJS(self):
        entrada = self.txtEntrada.get("1.0", END)  # fila 1 col 0 hasta fila 2 col 10
        miScanner = AnalizadorLexicoJS()
        retorno = miScanner.ScannerJS(entrada)
        self.txtConsola.delete("1.0", END)

        contadorT = 0
        contadorE = 0

        for i in range(0, len(miScanner.lista_Tokens)):
            contadorT += 1
            self.txtConsola.insert("1.0", f"{contadorT}. TOKEN: {miScanner.lista_Tokens[i].tipoToken.name} ,"
                                          f" VALOR: {miScanner.lista_Tokens[i].lexemaValor}\n")

        for i in range(0, len(miScanner.lista_ErroresLexicos)):
            contadorE += 1
            self.txtConsola.insert("1.0", f"{contadorE}. ERROR LEXICO: {miScanner.lista_ErroresLexicos[i].valor}, "
                                          f"POSICION: {miScanner.lista_ErroresLexicos[i].posicion.getPosicionH()} ,"
                                          f"{miScanner.lista_ErroresLexicos[i].posicion.posicionV}\n")

        messagebox.showinfo('Project 1', 'Analysis Finished')

    # Dispara el Filechooser
    def abrirArchivo(self):
        nameFile = filedialog.askopenfilename(title="Seleccione archivo", filetypes=
        (("js files", "*.js"), ("html files", "*.html"), ("css files", "*.css"), ("All Files", "*.*")))
        if nameFile != '':
            archi1 = open(nameFile, "r", encoding="utf-8")  # Lectura del archivo
            contenido = archi1.read()  # Obteniendo el texto / contenido
            archi1.close()  # Cerrando archivo
            self.txtEntrada.delete("1.0", END)
            self.txtEntrada.insert("1.0", contenido)
