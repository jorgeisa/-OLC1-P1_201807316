from tkinter import *  # ventana
from tkinter import Menu  # barra de tareas
from tkinter import filedialog  # filechooser
from tkinter import scrolledtext  # textarea
from tkinter import messagebox  # message box
from AnalizadorLexicoJS import AnalizadorLexicoJS


class PantallaAnalizador:
    # Metodo que contiene la definicion de la interfaz grafica
    def __init__(self):
        self.window = Tk()
        self.txtEntrada = Entry(self.window, width=10)
        self.txtConsola = Entry(self.window, width=10)

        # PROPIEDADES DE LA VENTANA, CENTRADO, TAMANIO, etc
        self.window.title("Proyecto 1 - Analizador Archivos")  # Titulo de la ventana
        widthTK = 800  # Ancho predeterminado de la ventana
        heightTK = 700  # Alura predeterminada de la ventana
        widthScreen = self.window.winfo_screenwidth()  # Ancho de la pantalla
        heightScreen = self.window.winfo_screenheight()  # Altura de la pantalla

        x = (widthScreen / 2) - (widthTK / 2)  # Posicion de centrado en x
        y = (heightScreen / 2) - (heightTK / 2)  # Posicion de centrado en y

        self.window.geometry('%dx%d+%d+%d' % (widthTK, heightTK, x, y - 25))  # Colocarle la vetana en el centro

        self.window.configure(bg='#75D578')  # Darle color a la ventana (fondo)

        # LABEL TITULO PROPIEDADES
        # Posicionandolo en la ventana, texto a mostrar, tipo letra, fondo del label
        self.lbl = Label(self.window, text="Analizador .JS, .CSS, .HTML", font=("Arial Bold", 15), bg='#0081AB')
        self.lbl.pack(fill=X)  # Label estirado por el eje X en su posicion

        # PROPIEDADES DEL MENU DESPLEGABLE
        # Agregando las opciones en el menu desplegable
        self.menu = Menu(self.window)
        self.file_item = Menu(self.menu)  # File
        self.file_item.add_command(label='Open File', command=self.abrirFile)
        self.file_item.add_separator()
        self.file_item.add_command(label='Analyze')
        self.file_item.add_separator()
        self.file_item.add_command(label='Exit')

        self.report_item = Menu(self.menu)  # Reports
        self.report_item.add_separator()
        self.report_item.add_command(label='Errors')
        self.report_item.add_separator()
        self.report_item.add_command(label='Tree')

        # Agregando estilo de menu - cascada
        self.menu.add_cascade(label='File', menu=self.file_item)
        self.menu.add_cascade(label='Reports', menu=self.report_item)

        # COLOCANDO EL MENU CON OPCIONES DENTRO DEL WINDOW
        self.window.config(menu=self.menu)

        # PROPIEDADES DEL TXTENTRADA (TEXTO A ANALIZAR)
        self.txtEntrada = scrolledtext.ScrolledText(self.window, width=80, height=25)
        self.txtEntrada.pack()
        self.txtEntrada.place(x=50, y=50)

        # PROPIEDADES DE LA CONSOLA, SALIDA (ANALISIS EXISTOSO, etc)
        self.lbl = Label(self.window, text="Console:")
        self.lbl.place(x=50, y=465)
        self.txtConsola = scrolledtext.ScrolledText(self.window, width=80, height=10, bg="#000000", fg="white")
        self.txtConsola.place(x=50, y=490)
        self.btn = Button(self.window, text="Analyze", bg="black", fg="white", command=self.Analyze)  # boton ANALYZE
        self.btn.place(x=655, y=460)

        # Dispara la interfaz y la mantiene abierta
        self.window.mainloop()

    def Analyze(self):
        entrada = self.txtEntrada.get("1.0", END)  # fila 1 col 0 hasta fila 2 col 10
        miScanner = AnalizadorLexicoJS()
        retorno = miScanner.ScannerJS(entrada)
        self.txtConsola.delete("1.0", END)
        self.txtConsola.insert("1.0", len(retorno))
        messagebox.showinfo('Project 1', 'Analysis Finished')

    # Dispara el Filechooser
    def abrirFile(self):
        nameFile = filedialog.askopenfilename(title="Seleccione archivo", filetypes=
        (("js files", "*.js"), ("html files", "*.html"), ("css files", "*.css"), ("All Files", "*.*")))
        if nameFile != '':
            archi1 = open(nameFile, "r", encoding="utf-8")  # Lectura del archivo
            contenido = archi1.read()  # Obteniendo el texto / contenido
            archi1.close()  # Cerrando archivo
            self.txtEntrada.delete("1.0", END)
            self.txtEntrada.insert("1.0", contenido)