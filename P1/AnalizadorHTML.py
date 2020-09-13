from Token import TipoTokenHTML
from Token import Token
from ErrorLexico import ErrorLexico
from Posicion import Posicion


class AnalizadorHTML:

    def __init__(self):
        self.lista_Tokens = list()
        self.lista_ErroresLexicos = list()
        self.entradaTexto = ""
        self.lexemaTemp = ""
        self.textoCorregido = ""
        self.pathSalida = ""
        self.contadorComentario = 0  # "Bandera para evalura el primer comentario para el path"
        self.contadorV = 1
        self.contadorH = 1
        self.posicion = 0

    def agregarToken(self, tipoToken, lexemaValor):
        self.lista_Tokens.append(Token(tipoToken, lexemaValor))
        self.textoCorregido += lexemaValor
        # self.estado = 0
        self.lexemaTemp = ""

    def agregarTokenNinguno(self, tipoToken, lexemaValor):
        self.lista_Tokens.append(Token(tipoToken, lexemaValor))

    def agregarError(self, valor, posicionColumna, posicionFila):
        self.lista_ErroresLexicos.append(ErrorLexico(valor, Posicion(posicionColumna, posicionFila)))

    def ScannerHTML(self, entrada):
        self.entradaTexto = f"{entrada}#"
        self.posicion = 0

        while self.posicion < len(self.entradaTexto):
            caracterActual = self.entradaTexto[self.posicion]

            # E0 -> E5
            if self.evaluarSimbolos():
                self.contadorH += 1
                self.posicion += 1

            # Comentario o solo abrir una etiqueta
            elif caracterActual == "<":
                self.estadoE6()

            # id o reservadas
            elif caracterActual.isalpha():
                finalActual = self.obtenerLongitud() + self.posicion
                self.estadoE3()
                self.posicion = finalActual

            # " E0 -> E4
            elif caracterActual == "\"":
                self.estadoE4()

            # E0 -> E13
            elif self.entradaTexto[self.posicion] == ">":
                self.estadoE13()

            elif caracterActual == " " or caracterActual == "\t" or caracterActual == "\n":
                if caracterActual == "\n":
                    self.contadorV += 1
                    self.contadorH = 1
                else:
                    self.contadorH += 1
                self.textoCorregido += caracterActual
                self.agregarToken(TipoTokenHTML.VALOR_INTERMEDIO, caracterActual)
                self.posicion += 1
                continue
            else:
                if (caracterActual == '#') and (self.posicion == (len(self.entradaTexto) - 1)):
                    print("Analisis HTML terminado!!")
                    print(f"Posicion: {self.contadorH}, {self.contadorV}")
                else:
                    print(f"Error Lexico. {caracterActual}")
                    self.agregarError(caracterActual, self.contadorH, self.contadorV)
                self.contadorH += 1
                self.posicion += 1

    # E0 -> E1 (N)
    def estadoE3(self):
        final = self.obtenerLongitud() + self.posicion
        for i in range(self.posicion, final):
            self.lexemaTemp += self.entradaTexto[i]

        # E0 -> E3
        if self.evaluarReservadas():
            self.contadorH += final
            return

        # E0 -> E1
        self.estadoE1(final)

    # ID E0 -> E1
    def estadoE1(self, final):
        self.lexemaTemp = ""
        while self.posicion < final:
            caracter = self.entradaTexto[self.posicion]

            if caracter.isalpha():
                self.lexemaTemp += caracter
            elif caracter.isnumeric():
                self.lexemaTemp += caracter
            else:
                self.agregarError(caracter, self.contadorH, self.contadorV)
                print(f"Error Lexico. {caracter}")
            if (self.posicion + 1) == final:
                if not self.evaluarReservadas():
                    self.agregarToken(TipoTokenHTML.ID, self.lexemaTemp)
            self.posicion += 1
            self.contadorH += 1

    def estadoE6(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        caracterActual = self.entradaTexto[self.posicion]

        # E6 -> E7
        if caracterActual == "!" and self.entradaTexto[self.posicion + 1] == "-" \
                and self.entradaTexto[self.posicion + 2] == "-":
            if self.contadorComentario != 3:
                self.contadorComentario += 1
            # implica comentario
            self.lexemaTemp += f"{caracterActual}{self.entradaTexto[self.posicion + 1]}{self.entradaTexto[self.posicion + 2]}"
            self.posicion += 3
            self.contadorH += 3
            self.estadoE9()

        # Estado E0 - > E6
        else:  # implica que es solo abrir una etiqueta
            self.agregarToken(TipoTokenHTML.SIMBOLO_INICIO_ETIQUETA, self.lexemaTemp)

    # E9 -> E9
    def estadoE9(self):
        while self.posicion < len(self.entradaTexto):
            caracter = self.entradaTexto[self.posicion]

            if caracter == "\n":
                self.agregarToken(TipoTokenHTML.COMENTARIO, self.lexemaTemp)

            # E9 -> E10 -> E11 -> E12
            elif caracter == "-" and self.entradaTexto[self.posicion + 1] == "-" and \
                    self.entradaTexto[self.posicion + 2] == ">":
                self.lexemaTemp += f"{caracter}"\
                                   f"{self.entradaTexto[self.posicion + 1]}{self.entradaTexto[self.posicion + 2]}"
                self.agregarToken(TipoTokenHTML.COMENTARIO, self.lexemaTemp)
                self.posicion += 3
                self.contadorH += 3
                return
            else:
                self.lexemaTemp += caracter

            if caracter == "C" and self.contadorComentario == 2:
                self.contadorComentario += 1
                contadorPath = self.posicion
                while self.entradaTexto[contadorPath] != "-" or self.entradaTexto[contadorPath + 1] != "-" \
                        or self.entradaTexto[contadorPath + 2] != ">":
                    self.pathSalida += self.entradaTexto[contadorPath]
                    contadorPath += 1
            self.posicion += 1
            self.contadorH += 1

    # E4 -> E2
    def estadoE4(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        while self.entradaTexto[self.posicion] != "\n":

            caracter = self.entradaTexto[self.posicion]
            self.lexemaTemp += caracter
            if caracter == "\"":
                self.agregarToken(TipoTokenHTML.CADENA, self.lexemaTemp)
                self.posicion += 1
                self.contadorH += 1
                return
            self.contadorH += 1
            self.posicion += 1
        self.agregarToken(TipoTokenHTML.CADENA, self.lexemaTemp)

    def estadoE13(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.agregarToken(TipoTokenHTML.SIMBOLO_FINAL_ETIQUETA, self.lexemaTemp)
        self.posicion += 1
        self.contadorH += 1
        final = self.obtenerLongitudAIgnorar() + self.posicion
        self.posicion = final

    # ----------------------        EVALUAR SIMBOLOS             ----------------------
    def evaluarSimbolos(self):
        caracterActual = self.entradaTexto[self.posicion]
        if caracterActual == "=":
            self.agregarToken(TipoTokenHTML.SIMBOLO_IGUAL, "=")
            return True
        elif caracterActual == "/":
            self.agregarToken(TipoTokenHTML.SIMBOLO_DIAGONAL, "/")
            return True
        return False

    # ----------------------     EVALUAR PALABRAS RESERVADAS     ----------------------
    def evaluarReservadas(self):
        if self.lexemaTemp.lower() == "html":
            self.agregarToken(TipoTokenHTML.RESERVADA, "html")
            return True
        elif self.lexemaTemp.lower() == "head":
            self.agregarToken(TipoTokenHTML.RESERVADA, "head")
            return True
        elif self.lexemaTemp.lower() == "title":
            self.agregarToken(TipoTokenHTML.RESERVADA, "title")
            return True
        elif self.lexemaTemp.lower() == "body":
            self.agregarToken(TipoTokenHTML.RESERVADA, "body")
            return True
        elif self.lexemaTemp.lower() == "img":
            self.agregarToken(TipoTokenHTML.RESERVADA, "img")
            return True
        elif self.lexemaTemp.lower() == "a":
            self.agregarToken(TipoTokenHTML.RESERVADA, "a")
            return True
        elif self.lexemaTemp.lower() == "ol":
            self.agregarToken(TipoTokenHTML.RESERVADA, "ol")
            return True
        elif self.lexemaTemp.lower() == "ul":
            self.agregarToken(TipoTokenHTML.RESERVADA, "ul")
            return True
        elif self.lexemaTemp.lower() == "style":
            self.agregarToken(TipoTokenHTML.RESERVADA, "style")
            return True
        elif self.lexemaTemp.lower() == "p":
            self.agregarToken(TipoTokenHTML.RESERVADA, "p")
            return True
        elif self.lexemaTemp.lower() == "table":
            self.agregarToken(TipoTokenHTML.RESERVADA, "table")
            return True
        elif self.lexemaTemp.lower() == "th":
            self.agregarToken(TipoTokenHTML.RESERVADA, "th")
            return True
        elif self.lexemaTemp.lower() == "tr":
            self.agregarToken(TipoTokenHTML.RESERVADA, "tr")
            return True
        elif self.lexemaTemp.lower() == "td":
            self.agregarToken(TipoTokenHTML.RESERVADA, "td")
            return True
        elif self.lexemaTemp.lower() == "caption":
            self.agregarToken(TipoTokenHTML.RESERVADA, "caption")
            return True
        elif self.lexemaTemp.lower() == "colgroup":
            self.agregarToken(TipoTokenHTML.RESERVADA, "colgroup")
            return True
        elif self.lexemaTemp.lower() == "col":
            self.agregarToken(TipoTokenHTML.RESERVADA, "col")
            return True
        elif self.lexemaTemp.lower() == "thead":
            self.agregarToken(TipoTokenHTML.RESERVADA, "thead")
            return True
        elif self.lexemaTemp.lower() == "tbody":
            self.agregarToken(TipoTokenHTML.RESERVADA, "tbody")
            return True
        elif self.lexemaTemp.lower() == "tfoot":
            self.agregarToken(TipoTokenHTML.RESERVADA, "tfoot")
            return True

    # ----------------------    Obtener la longitud del > longitud <     ----------------------
    # E13 -> E13
    def obtenerLongitudAIgnorar(self):
        contador = 0
        for i in range(self.posicion, len(self.entradaTexto) - 1):
            if self.entradaTexto[i] == "<":
                self.contadorH -= 1
                # E13 -> E14
                break
            if self.entradaTexto[i] == "\n":
                self.contadorV += 1
                self.contadorH = 1
            contador += 1
            self.contadorH += 1
            self.lexemaTemp += self.entradaTexto[i]
        self.agregarToken(TipoTokenHTML.VALOR_INTERMEDIO, self.lexemaTemp)
        return contador

    def obtenerLongitud(self):
        contador = 0
        for i in range(self.posicion, len(self.entradaTexto) - 1):
            if self.entradaTexto[i] == " " or self.entradaTexto[i] == "\t" or self.entradaTexto[i] == "\n" \
                    or self.entradaTexto[i] == "\r" or self.entradaTexto[i] == ">" or self.entradaTexto[i] == "\"" \
                    or self.entradaTexto[i] == "=" or self.entradaTexto[i] == "/":
                break
            contador += 1
        return contador

    def imprimirErrores(self):
        contador = 0
        for i in range(0, len(self.lista_ErroresLexicos)):
            contador += 1
            print(f"{contador}. ERROR LEXICO: {self.lista_ErroresLexicos[i].valor}, "
                  f"POSICION: {self.lista_ErroresLexicos[i].posicion.getPosicionH()} ,"
                  f"{self.lista_ErroresLexicos[i].posicion.posicionV}")

    def imprimirTokens(self):
        contador = 0
        for i in range(0, len(self.lista_Tokens)):
            contador += 1
            print(
                f"{contador}. TOKEN: {self.lista_Tokens[i].tipoToken.name} , VALOR: {self.lista_Tokens[i].lexemaValor}")
