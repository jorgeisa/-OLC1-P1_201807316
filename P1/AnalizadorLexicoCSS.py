class AnalizadorLexicoCSS:
    def __init__(self):
        self.lista_Tokens = list()
        self.lista_ErroresLexicos = list()
        self.entradaTexto = ""
        self.lexemaTemp = ""
        self.contadorV = 1
        self.contadorH = 1
        self.posicion = 0