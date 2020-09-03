from Token import TipoToken
from Token import Token


class AnalizadorLexicoJS():

    def __init__(self):
        self.lista_Tokens = list()
        self.lista_ErroresLexicos = list()
        self.entradaTexto = ""
        self.lexemaTemp = ""
        self.estado = 0
        self.posicion = 0

    def agregarToken(self, tipoToken, lexemaValor):
        self.lista_Tokens.append(Token(tipoToken, lexemaValor))
        self.estado = 0
        self.lexemaTemp = ""

    def ScannerJS(self, entrada):
        self.entradaTexto += f"{entrada}#"
        self.posicion = 0

        while self.posicion < len(self.entradaTexto):

            caracterActual = self.entradaTexto[self.posicion]
            print(caracterActual)

            # q0 -> q7
            if self.estado == 0:
                if caracterActual == ",":
                    self.agregarToken(TipoToken.SIMBOLO_COMA, ",")
                elif caracterActual == ";":
                    self.agregarToken(TipoToken.SIMBOLO_PUNTO_COMA, ";")
                elif caracterActual == ":":
                    self.agregarToken(TipoToken.SIMBOLO_DOS_PUNTOS, ":")
                elif caracterActual == "{":
                    self.agregarToken(TipoToken.SIMBOLO_LLAVE_ABRE, "{")
                elif caracterActual == "}":
                    self.agregarToken(TipoToken.SIMBOLO_LLAVE_CIERRA, "}")
                elif caracterActual == "(":
                    self.agregarToken(TipoToken.SIMBOLO_PARENTESIS_ABRE, "(")
                elif caracterActual == ")":
                    self.agregarToken(TipoToken.SIMBOLO_PARENTESIS_CIERRA, ")")

                elif caracterActual.isnumeric():
                    self.estadoE1()
                elif caracterActual.isalpha():
                    finalActual = self.obtenerLongitud() + self.posicion
                    self.estadoE6()
                    self.posicion = (finalActual - 1)  # poner fuera del metodo
                elif caracterActual == "/":  # comentario
                    self.estadoE8()
                elif caracterActual == " " or caracterActual == "\t" or caracterActual == "\n":
                    self.posicion += 1
                    continue
                else:
                    if (caracterActual == '#') and (self.posicion == (len(self.entradaTexto) - 1)):
                        print(len(self.entradaTexto))
                        self.imprimirTokens()
                        print("analisis finalizado")
                    else:
                        print(f"Error Lexico. {caracterActual}")
                        self.lista_ErroresLexicos.append(caracterActual)
                        #  self.agregarToken(TipoToken.DESCONOCIDO, caracterActual)
            self.posicion += 1
        return self.lista_Tokens

    # ----------------------     NUMEROS   ----------------------
    def estadoE1(self):  # numeros
        final = self.obtenerLongitud() + self.posicion
        #  final siempre sera una unidad mas grande de donde se debe parar
        while self.posicion < final:
            caracter = self.entradaTexto[self.posicion]
            if caracter.isnumeric():
                self.lexemaTemp += caracter
            else:
                self.lista_ErroresLexicos.append(caracter)
                print(f"Error Lexico: {caracter}")

            if self.posicion + 1 == final:
                self.agregarToken(TipoToken.NUMERO_ENTERO, self.lexemaTemp)
            self.posicion += 1  # Para recorrer el while
        self.posicion = (final - 1)

    # ----------------------     PALABRAS RESERVADAS   ----------------------
    def estadoE6(self):  # letra | ID | RESERVADAS
        final = self.obtenerLongitud() + self.posicion
        for i in range(self.posicion, final):
            self.lexemaTemp += self.entradaTexto[i]
        #  print(f"Impresion {self.entradaTexto[final]} , {final}, {self.entradaTexto}")
        #  print(f"AQUI ES LA IMPRESION {self.lexemaTemp}, {self.posicion}")
        if self.evaluarReservadas():
            return

        self.estadoE2(final)

    def estadoE2(self, final):
        self.lexemaTemp = ""
        while self.posicion < final:
            caracter = self.entradaTexto[self.posicion]

            if caracter.isalpha():
                self.lexemaTemp += caracter
            elif caracter.isnumeric():
                self.lexemaTemp += caracter
            else:
                self.lista_ErroresLexicos.append(caracter)
                #  self.agregarToken(TipoToken.DESCONOCIDO, caracter)
                print(f"Error Lexico. {caracter}")
            if self.posicion + 1 == final:
                if not self.evaluarReservadas():
                    self.agregarToken(TipoToken.ID, self.lexemaTemp)
            self.posicion += 1

    # ----------------------     COMENTARIOS     ----------------------
    def estadoE8(self):  # comentarios
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        while self.posicion < len(self.entradaTexto):
            caracter = self.entradaTexto[self.posicion]
            if caracter == "/":
                self.lexemaTemp += caracter
                self.posicion += 1
                self.estadoE9()
                return
            elif caracter == "*":
                self.lexemaTemp += caracter
                self.posicion += 1
                self.estadoE10()
                return
            else:
                self.lista_ErroresLexicos.append(caracter)
                print(f"Error Lexico: {caracter}")
            self.posicion += 1

    def estadoE9(self):
        while self.posicion < len(self.entradaTexto):
            caracter = self.entradaTexto[self.posicion]
            if caracter == "\n":
                self.agregarToken(TipoToken.COMENTARIO_UNILINEA, self.lexemaTemp)
                self.posicion -= 1
                return
            else:
                self.lexemaTemp += caracter
            self.posicion += 1

    def estadoE10(self):
        while self.posicion < len(self.entradaTexto):
            caracter = self.entradaTexto[self.posicion]
            if caracter == "*":
                self.lexemaTemp += caracter
                if self.entradaTexto[self.posicion+1] == "/":
                    self.posicion += 1
                    self.lexemaTemp += self.entradaTexto[self.posicion]
                    self.agregarToken(TipoToken.COMENTARIO_MULTILINEA, self.lexemaTemp)
                    return
            else:
                self.lexemaTemp += caracter
            self.posicion += 1
        self.posicion -= 2
        self.lista_ErroresLexicos.append(self.lexemaTemp)
        print(f"Error lexico: {self.lexemaTemp}")
        self.lexemaTemp = ""

    # ----------------------     EVALUAR PALABRAS RESERVADAS     ----------------------
    def evaluarReservadas(self):
        if self.lexemaTemp.lower() == "return":
            self.agregarToken(TipoToken.RESERVADA_RETURN, "return")
            return True
        elif self.lexemaTemp.lower() == "break":
            self.agregarToken(TipoToken.RESERVADA_BREAK, "break")
            return True
        elif self.lexemaTemp.lower() == "continue":
            self.agregarToken(TipoToken.RESERVADA_CONTINUE, "continue")
            return True
        elif self.lexemaTemp.lower() == "do":
            self.agregarToken(TipoToken.RESERVADA_DO, "do")
            return True
        elif self.lexemaTemp.lower() == "while":
            self.agregarToken(TipoToken.RESERVADA_WHILE, "while")
            return True
        elif self.lexemaTemp.lower() == "for":
            self.agregarToken(TipoToken.RESERVADA_FOR, "for")
            return True
        elif self.lexemaTemp.lower() == "if":
            self.agregarToken(TipoToken.RESERVADA_IF, "if")
            return True
        elif self.lexemaTemp.lower() == "var":
            self.agregarToken(TipoToken.RESERVADA_VAR, "var")
            return True
        return False

    # ----------------------     OBTENER LAL ONGITUD ANTES DE UN ESPACIO, ETC     ----------------------
    def obtenerLongitud(self):
        contador = 0
        for i in range(self.posicion, len(self.entradaTexto) - 1):
            if self.entradaTexto[i] == " " or self.entradaTexto[i] == "\t" or self.entradaTexto[i] == "\n" \
                    or self.entradaTexto[i] == "\r" or self.entradaTexto[i] == "{" or self.entradaTexto[i] == "}" \
                    or self.entradaTexto[i] == "(" or self.entradaTexto[i] == ")" or self.entradaTexto[i] == ";" \
                    or self.entradaTexto[i] == "," or self.entradaTexto[i] == ":" or self.entradaTexto[i] == "+" \
                    or self.entradaTexto[i] == "-" or self.entradaTexto[i] == "*" or self.entradaTexto[i] == ".":
                break
            contador += 1
        return contador

    def imprimirTokens(self):
        contador = 0
        for i in range(0, len(self.lista_Tokens)):
            contador += 1
            print(
                f"{contador}. TOKEN: {self.lista_Tokens[i].tipoToken.name} , VALOR: {self.lista_Tokens[i].lexemaValor}")
