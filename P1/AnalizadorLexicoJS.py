from Token import TipoToken
from Token import Token
from ErrorLexico import ErrorLexico
from Posicion import Posicion


class AnalizadorLexicoJS:

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

    def ScannerJS(self, entrada):
        self.entradaTexto += f"{entrada}#"
        self.posicion = 0

        while self.posicion < (len(self.entradaTexto)):

            caracterActual = self.entradaTexto[self.posicion]
            # print(caracterActual)

            # E0 -> E7
            # if self.estado == 0:
            if self.evaluarSimbolos():
                self.posicion += 1
                self.contadorH += 1
                caracterActual = self.entradaTexto[self.posicion]

            # E0 -> E Simbolos "Especiales"
            elif caracterActual == "+":
                self.estadoE13()
            elif caracterActual == "=":
                self.estadoE14()
            elif caracterActual == ">":
                self.estadoE15()
            elif caracterActual == "<":
                self.estadoE22()
            elif caracterActual == "*":
                self.estadoE16()
            elif caracterActual == "!":
                self.estadoE17()
            elif caracterActual == "&":
                self.estadoE18()
            elif caracterActual == "|":
                self.estadoE19()

            # E0 -> E1
            elif caracterActual.isnumeric():  # NUMERO ENTERO
                self.estadoE1()

            # E0 -> E6
            elif caracterActual.isalpha():  # ID | RESERVADAS
                finalActual = self.obtenerLongitud() + self.posicion
                self.estadoE6()
                self.posicion = finalActual  # poner fuera del metodo

            # E0 -> E8
            elif caracterActual == "/":  # comentario , /
                self.estadoE8()
            # E0 -> E cadenas
            elif caracterActual == "'":
                self.estadoE20()
            # E0 -> E cadenas
            elif caracterActual == "\"":
                self.estadoE21()
            # E0 -> E0
            elif caracterActual == " " or caracterActual == "\t" or caracterActual == "\n":
                if caracterActual == "\n":
                    self.contadorV += 1
                    self.contadorH = 1
                else:
                    self.contadorH += 1
                self.textoCorregido += caracterActual
                self.agregarTokenNinguno(TipoToken.NINGUNO, caracterActual)
                self.posicion += 1
                continue
            else:
                if (caracterActual == '#') and (self.posicion == (len(self.entradaTexto) - 1)):
                    # print(len(self.entradaTexto))
                    # self.imprimirTokens()
                    # print("----------------------")
                    # self.imprimirErrores()
                    print("analisis JS finalizado")
                    print(f"Posicion: {self.contadorH}, {self.contadorV}")
                else:
                    print(f"Error Lexico. {caracterActual}")
                    self.agregarError(caracterActual, self.contadorH, self.contadorV)
                self.contadorH += 1
                self.posicion += 1

            # self.posicion += 1
        return self.lista_Tokens

    # ----------------------     NUMEROS   ----------------------
    def estadoE1(self):  # numeros  111,111
        final = self.obtenerLongitud() + self.posicion

        #  final siempre sera una unidad mas grande de donde se debe parar
        while self.posicion < final:
            caracter = self.entradaTexto[self.posicion]
            if caracter.isnumeric():
                self.lexemaTemp += caracter
            else:
                # self.contadorH-1
                self.agregarError(caracter, self.contadorH, self.contadorV)
                print(f"Error Lexico: {caracter}")

            if self.posicion + 1 == final:
                self.agregarToken(TipoToken.NUMERO_ENTERO, self.lexemaTemp)
            self.posicion += 1  # Para recorrer el while
            self.contadorH += 1
        self.posicion = final

    # ----------------------     PALABRAS RESERVADAS   ----------------------
    def estadoE6(self):  # letra | ID | RESERVADAS
        final = self.obtenerLongitud() + self.posicion
        for i in range(self.posicion, final):
            self.lexemaTemp += self.entradaTexto[i]

        if self.evaluarReservadas():
            self.contadorH += self.obtenerLongitud()
            return

        self.estadoE2(final)

    def estadoE2(self, final):
        self.lexemaTemp = ""  # 40,41,42,43,44,45,46,  47       ,48,49,50
        while self.posicion < final:  # id4@3id  0 - 6
            caracter = self.entradaTexto[self.posicion]

            if caracter.isalpha():
                self.lexemaTemp += caracter
            elif caracter.isnumeric():
                self.lexemaTemp += caracter
            elif caracter == "_":
                self.lexemaTemp += caracter
            else:
                # self.contadorH-1
                self.agregarError(caracter, self.contadorH, self.contadorV)
                print(f"Error Lexico. {caracter}")
            if (self.posicion + 1) == final:
                if not self.evaluarReservadas():
                    self.agregarToken(TipoToken.ID, self.lexemaTemp)
            self.posicion += 1
            self.contadorH += 1

    # ----------------------     COMENTARIOS     ----------------------
    def estadoE8(self):  # comentarios
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        caracter = self.entradaTexto[self.posicion]
        if caracter == "/":
            # Para el path del comentario
            if self.contadorComentario != 3:
                self.contadorComentario += 1
            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            self.estadoE9()
            return
        elif caracter == "*":
            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            self.estadoE10()
            return
        else:
            self.agregarToken(TipoToken.SIGNO_DIVISION, self.lexemaTemp)
            return

    # Comentario unilinea
    def estadoE9(self):
        #  //COMENTARIO    C
        while self.posicion < len(self.entradaTexto):
            caracter = self.entradaTexto[self.posicion]

            if caracter == "\n":
                self.agregarToken(TipoToken.COMENTARIO_UNILINEA, self.lexemaTemp)
                return
            else:
                self.lexemaTemp += caracter
            # Recuperar Path de Salida
            if caracter == "C" and self.contadorComentario == 2:
                self.contadorComentario += 1
                contadorPath = self.posicion
                while self.entradaTexto[contadorPath] != "\n":
                    self.pathSalida += self.entradaTexto[contadorPath]
                    contadorPath += 1

            self.posicion += 1
            self.contadorH += 1

    def estadoE10(self):
        while self.posicion < (len(self.entradaTexto) - 1):
            caracter = self.entradaTexto[self.posicion]
            if caracter == "*":
                self.lexemaTemp += caracter
                if self.entradaTexto[self.posicion + 1] == "/":
                    self.lexemaTemp += self.entradaTexto[self.posicion + 1]
                    self.posicion += 2
                    self.contadorH += 2
                    self.agregarToken(TipoToken.COMENTARIO_MULTILINEA, self.lexemaTemp)
                    return
            else:
                self.lexemaTemp += caracter
                if caracter == "\n":
                    self.contadorV += 1
            self.posicion += 1
            self.contadorH += 1
        self.posicion -= 1
        self.contadorH -= 1
        self.agregarToken(TipoToken.COMENTARIO_MULTILINEA, self.lexemaTemp)
        print(f"No se detecto */")
        self.lexemaTemp = ""

    # Estado E13 + , +=, ++
    def estadoE13(self):  # += , ++
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1

        caracter = self.entradaTexto[self.posicion]

        if caracter == "=":
            self.lexemaTemp += caracter
            self.agregarToken(TipoToken.SIMBOLO_ASIGNACION_ADICION, self.lexemaTemp)
        elif caracter == "+":
            self.lexemaTemp += caracter
            self.agregarToken(TipoToken.SIMBOLO_INCREMENTO, self.lexemaTemp)
        else:
            self.agregarToken(TipoToken.SIGNO_SUMA, self.lexemaTemp)
            self.posicion -= 1
            self.contadorH -= 1
        self.posicion += 1
        self.contadorH += 1

    # == , ===, =>, =
    def estadoE14(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        caracter = self.entradaTexto[self.posicion]

        if caracter == "=":  # = =
            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            caracter = self.entradaTexto[self.posicion]  # == =
            if caracter == "=":
                self.lexemaTemp += caracter
                self.posicion += 1
                self.contadorH += 1
                self.agregarToken(TipoToken.SIMBOLO_ESTRICTAMENTE_IGUALES, self.lexemaTemp)
            else:
                self.agregarToken(TipoToken.RELACIONAL_IGUAL, self.lexemaTemp)
        elif caracter == ">":
            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            self.agregarToken(TipoToken.SIMBOLO_LAMBDA, self.lexemaTemp)
        else:
            self.agregarToken(TipoToken.SIMBOLO_IGUAL, self.lexemaTemp)

    def estadoE15(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        caracter = self.entradaTexto[self.posicion]

        if caracter == "=":
            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            self.agregarToken(TipoToken.RELACIONAL_MAYOR_IGUAL, self.lexemaTemp)
        else:
            self.agregarToken(TipoToken.SIMBOLO_MAYOR_QUE, self.lexemaTemp)

    def estadoE16(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        caracter = self.entradaTexto[self.posicion]

        if caracter == "=":
            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            self.agregarToken(TipoToken.SIMBOLO_ASIGNACION_MULTIPLICACION, self.lexemaTemp)
        else:
            self.agregarToken(TipoToken.SIGNO_MULTIPLICACION, self.lexemaTemp)

    def estadoE17(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        caracter = self.entradaTexto[self.posicion]

        if caracter == "=":
            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            self.agregarToken(TipoToken.RELACIONAL_DISTINTO, self.lexemaTemp)
        else:
            self.agregarToken(TipoToken.SIMBOLO_NEGACION, self.lexemaTemp)

    def estadoE18(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        caracter = self.entradaTexto[self.posicion]
        if caracter == "&":
            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            self.agregarToken(TipoToken.LOGICO_CONJUNCION, self.lexemaTemp)
        else:
            print(f"Error Lexico: {self.lexemaTemp}")
            self.agregarError(self.lexemaTemp, self.contadorH, self.contadorV)
            self.contadorH += 1
        self.lexemaTemp = ""

    def estadoE19(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        caracter = self.entradaTexto[self.posicion]
        if caracter == "|":
            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            self.agregarToken(TipoToken.LOGICO_DISYUNCION, self.lexemaTemp)
        else:
            print(f"Error Lexico: {self.lexemaTemp}")
            self.agregarError(self.lexemaTemp, self.contadorH, self.contadorV)
        self.lexemaTemp = ""

    def estadoE20(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        while self.entradaTexto[self.posicion] != "\n":
            caracter = self.entradaTexto[self.posicion]
            self.lexemaTemp += caracter
            if caracter == "'":
                self.agregarToken(TipoToken.CADENA_SIMPLES, self.lexemaTemp)
                self.posicion += 1
                self.contadorH += 1
                return
            self.posicion += 1
            self.contadorH += 1
        self.agregarToken(TipoToken.CADENA_SIMPLES, self.lexemaTemp)

    def estadoE21(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        while self.entradaTexto[self.posicion] != "\n":
            caracter = self.entradaTexto[self.posicion]
            self.lexemaTemp += caracter
            if caracter == "\"":
                self.agregarToken(TipoToken.CADENA_DOBLES, self.lexemaTemp)
                self.posicion += 1
                self.contadorH += 1
                return
            self.contadorH += 1
            self.posicion += 1
        self.agregarToken(TipoToken.CADENA_DOBLES, self.lexemaTemp)

    def estadoE22(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        caracter = self.entradaTexto[self.posicion]

        if caracter == "=":
            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            self.agregarToken(TipoToken.RELACIONAL_MENOR_IGUAL, self.lexemaTemp)
        else:
            self.agregarToken(TipoToken.SIMBOLO_MENOR_QUE, self.lexemaTemp)

    # ----------------------        EVALUAR SIMBOLOS             ----------------------
    def evaluarSimbolos(self):
        caracterActual = self.entradaTexto[self.posicion]
        if caracterActual == ",":
            self.agregarToken(TipoToken.SIMBOLO_COMA, ",")
            return True
        elif caracterActual == ";":
            self.agregarToken(TipoToken.SIMBOLO_PUNTO_COMA, ";")
            return True
        elif caracterActual == ":":
            self.agregarToken(TipoToken.SIMBOLO_DOS_PUNTOS, ":")
            return True
        elif caracterActual == "{":
            self.agregarToken(TipoToken.SIMBOLO_LLAVE_ABRE, "{")
            return True
        elif caracterActual == "}":
            self.agregarToken(TipoToken.SIMBOLO_LLAVE_CIERRA, "}")
            return True
        elif caracterActual == "(":
            self.agregarToken(TipoToken.SIMBOLO_PARENTESIS_ABRE, "(")
            return True
        elif caracterActual == ")":
            self.agregarToken(TipoToken.SIMBOLO_PARENTESIS_CIERRA, ")")
            return True
        elif caracterActual == ".":
            self.agregarToken(TipoToken.SIMBOLO_PUNTO, ".")
            return True
        elif caracterActual == "-":
            self.agregarToken(TipoToken.SIGNO_RESTA, "-")
            return True
        return False

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
        elif self.lexemaTemp.lower() == "math":
            self.agregarToken(TipoToken.RESERVADA_VAR, "Math")
            return True
        elif self.lexemaTemp.lower() == "pow":
            self.agregarToken(TipoToken.RESERVADA_VAR, "pow")
            return True
        return False

    # ----------------------     OBTENER LA LONGITUD ANTES DE UN ESPACIO, ETC     ----------------------
    def obtenerLongitud(self):
        contador = 0
        for i in range(self.posicion, len(self.entradaTexto) - 1):
            if self.entradaTexto[i] == " " or self.entradaTexto[i] == "\t" or self.entradaTexto[i] == "\n" \
                    or self.entradaTexto[i] == "\r" or self.entradaTexto[i] == "{" or self.entradaTexto[i] == "}" \
                    or self.entradaTexto[i] == "(" or self.entradaTexto[i] == ")" or self.entradaTexto[i] == ";" \
                    or self.entradaTexto[i] == "," or self.entradaTexto[i] == ":" or self.entradaTexto[i] == "+" \
                    or self.entradaTexto[i] == "-" or self.entradaTexto[i] == "*" or self.entradaTexto[i] == "." \
                    or self.entradaTexto[i] == "<" or self.entradaTexto[i] == ">" or self.entradaTexto[i] == "=" \
                    or self.entradaTexto[i] == "!" or self.entradaTexto[i] == "/" or self.entradaTexto[i] == ":" \
                    or self.entradaTexto[i] == "&" or self.entradaTexto[i] == "|":
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
