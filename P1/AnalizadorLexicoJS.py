from graphviz import Digraph

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
        self.dotAFD1 = Digraph(comment="Grafica1", format='jpg')
        self.dotAFD2 = Digraph(comment="Grafica2", format='jpg')
        self.dotAFD3 = Digraph(comment="Grafica3", format='jpg')
        self.boolGrafo1 = False
        self.boolGrafo2 = False
        self.boolReservada = False
        self.boolGrafo3 = False

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
            # E0-> E13 , E14, E15, E16, E17, E18, E19, E22
            # E22, E23, E24, E25, E26, E27, E29, E31, E32
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

            # E0 -> E6, E2,
            elif caracterActual.isalpha():  # ID | RESERVADAS
                finalActual = self.obtenerLongitud() + self.posicion
                self.estadoE6()
                self.posicion = finalActual  # poner fuera del metodo
                if not self.boolGrafo2:
                    self.boolGrafo2 = True
                    self.dotAFD2.render(filename="AFD 2")

            # E0 -> E8, E10, E11, E12, E9
            elif caracterActual == "/":  # comentario , /
                self.estadoE8()
            # E0 -> E20, E28 cadenas
            elif caracterActual == "'":
                self.estadoE20()
            # E0 -> E21, EE30 cadenas
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
            # E1 0> E1
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
    # E0 -> E6 ("/")
    def estadoE6(self):  # letra | ID | RESERVADAS
        if not self.boolGrafo2:
            self.dotAFD2.attr(rankdir='LR')
            self.dotAFD2.node("0", label="E0", shape="circle")
            self.dotAFD2.node("2", label="E2", shape="doublecircle")

        final = self.obtenerLongitud() + self.posicion
        for i in range(self.posicion, final):
            self.lexemaTemp += self.entradaTexto[i]

        # E0 -> E6
        if self.evaluarReservadas():
            if not self.boolGrafo2:
                self.dotAFD2.edge("0", "2", self.entradaTexto[self.posicion])
                for i in range(self.posicion, final):
                    if (self.posicion + 1) != final:
                        self.dotAFD2.edge("2", "2", self.entradaTexto[i + 1], dir="forward")
            self.contadorH += self.obtenerLongitud()
            return

        # E0 -> E2
        self.estadoE2(final)

    # E2 -> E2
    def estadoE2(self, final):
        self.lexemaTemp = ""  # 40,41,42,43,44,45,46,  47       ,48,49,50

        if not self.boolGrafo2:
            self.dotAFD2.edge("0", "2", self.entradaTexto[self.posicion])

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

            if not self.boolGrafo2:
                if self.entradaTexto[self.posicion + 1].isalpha() and (self.posicion + 1) != final:
                    self.dotAFD2.edge("2", "2", self.entradaTexto[self.posicion + 1])
                elif self.entradaTexto[self.posicion + 1].isnumeric() and (self.posicion + 1) != final:
                    self.dotAFD2.edge("2", "2", self.entradaTexto[self.posicion + 1])
                elif self.entradaTexto[self.posicion + 1] == "_" and (self.posicion + 1) != final:
                    self.dotAFD2.edge("2", "2", self.entradaTexto[self.posicion + 1])

            self.posicion += 1
            self.contadorH += 1

    # ----------------------     COMENTARIOS     ----------------------
    # E0 -> E8
    def estadoE8(self):  # comentarios
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        caracter = self.entradaTexto[self.posicion]
        if caracter == "/":
            # Para el path del comentario
            if self.contadorComentario != 3:
                self.contadorComentario += 1

            # if self.boolGrafo3:
            #     self.dotAFD3.node("9", label="E9", shape="circle")
            #     self.dotAFD3.edge("8", "9", f"{caracter}")

            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            # E8-> E9
            self.estadoE9()
            return
        elif caracter == "*":
            if not self.boolGrafo3:
                self.dotAFD3.attr(rankdir="LR")
                self.dotAFD3.node("0", label="E0", shape="circle")
                self.dotAFD3.node("8", label="E8", shape="circle")
                self.dotAFD3.edge("0", "8", f"{self.entradaTexto[self.posicion-1]}")

                self.dotAFD3.node("10", label="E10", shape="circle")
                self.dotAFD3.edge("8", "10", f"{caracter}")

            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            # E8-> E10
            self.estadoE10()
            return
        else:
            self.agregarToken(TipoToken.SIGNO_DIVISION, self.lexemaTemp)
            return

    # Comentario unilinea
    # E9 -> E9
    def estadoE9(self):
        #  //COMENTARIO    C
        while self.posicion < len(self.entradaTexto):
            caracter = self.entradaTexto[self.posicion]

            if caracter == "\n":
                self.agregarToken(TipoToken.COMENTARIO_UNILINEA, self.lexemaTemp)
                return
            else:
                # if self.boolGrafo3:
                #     self.dotAFD3.edge("9", "9", f"{caracter}")
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

    # E10 -> E10
    def estadoE10(self):
        while self.posicion < (len(self.entradaTexto) - 1):
            caracter = self.entradaTexto[self.posicion]
            if caracter == "*":
                # E11
                if not self.boolGrafo3:
                    self.dotAFD3.node("11", label="E11", shape="circle")
                    self.dotAFD3.edge("10", "11", f"{caracter}")

                self.lexemaTemp += caracter
                if self.entradaTexto[self.posicion + 1] == "/":
                    # E11-> E12
                    if not self.boolGrafo3:
                        self.dotAFD3.node("12", label="E12", shape="doublecircle")
                        self.dotAFD3.edge("11", "12", f"{self.entradaTexto[self.posicion + 1]}")

                    self.lexemaTemp += self.entradaTexto[self.posicion + 1]
                    self.posicion += 2
                    self.contadorH += 2
                    self.agregarToken(TipoToken.COMENTARIO_MULTILINEA, self.lexemaTemp)
                    if not self.boolGrafo3:
                        self.boolGrafo3 = True
                        self.dotAFD3.render(filename="AFD 3")
                    return
                # E11 -> E10
            else:
                if not self.boolGrafo3:
                    self.dotAFD3.edge("10", "10", f"{caracter}")

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

    # E0 -> E20 (')
    def estadoE20(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        while self.entradaTexto[self.posicion] != "\n":
            # E20 -> E20
            caracter = self.entradaTexto[self.posicion]
            self.lexemaTemp += caracter
            if caracter == "'":
                # E20 -> E28
                self.agregarToken(TipoToken.CADENA_SIMPLES, self.lexemaTemp)
                self.posicion += 1
                self.contadorH += 1
                return
            self.posicion += 1
            self.contadorH += 1
        self.agregarToken(TipoToken.CADENA_SIMPLES, self.lexemaTemp)

    # E0 -> E21 (")
    def estadoE21(self):
        if not self.boolGrafo1:
            self.dotAFD1.attr(rankdir='LR')
            self.dotAFD1.node(f"0", label="E0", shape="circle")
            self.dotAFD1.node(f"21", label="E21", shape="circle", width="1")
            self.dotAFD1.edge("0", "21", "\" Comillas")
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        while self.entradaTexto[self.posicion] != "\n":
            # E21 -> E21
            caracter = self.entradaTexto[self.posicion]
            self.lexemaTemp += caracter
            if caracter == "\"":
                # E21 -> E30
                if not self.boolGrafo1:
                    self.boolGrafo1 = True
                    self.dotAFD1.node("30", label='E30', shape="doublecircle")
                    self.dotAFD1.edge("21", "30", "\" Comillas")
                    self.dotAFD1.render(filename="AFD 1")
                self.agregarToken(TipoToken.CADENA_DOBLES, self.lexemaTemp)
                self.posicion += 1
                self.contadorH += 1
                return
            self.dotAFD1.edge("21", "21", f"{caracter}", dir='forward')
            self.contadorH += 1
            self.posicion += 1
        if not self.boolGrafo1:
            self.boolGrafo1 = True
            self.dotAFD1.node("30", label='E30', shape="doublecircle")
            self.dotAFD1.edge("21", "30", "Fin")
            self.dotAFD1.render(filename="AFD 1")
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
            if self.boolGrafo2:
                self.dotAFD2.node("6", label="E6", shape="doublecircle")
                self.dotAFD2.edge("0", "6", "return")
            return True
        elif self.lexemaTemp.lower() == "break":
            self.agregarToken(TipoToken.RESERVADA_BREAK, "break")
            if self.boolGrafo2:
                self.dotAFD2.node("6", label="E6", shape="doublecircle")
                self.dotAFD2.edge("0", "6", "break")
            return True
        elif self.lexemaTemp.lower() == "continue":
            self.agregarToken(TipoToken.RESERVADA_CONTINUE, "continue")
            if self.boolGrafo2:
                self.dotAFD2.node("6", label="E6", shape="doublecircle")
                self.dotAFD2.edge("0", "6", "continue")
            return True
        elif self.lexemaTemp.lower() == "do":
            self.agregarToken(TipoToken.RESERVADA_DO, "do")
            if self.boolGrafo2:
                self.dotAFD2.node("6", label="E6", shape="doublecircle")
                self.dotAFD2.edge("0", "6", "do")
            return True
        elif self.lexemaTemp.lower() == "while":
            self.agregarToken(TipoToken.RESERVADA_WHILE, "while")
            if self.boolGrafo2:
                self.dotAFD2.node("6", label="E6", shape="doublecircle")
                self.dotAFD2.edge("0", "6", "while")
            return True
        elif self.lexemaTemp.lower() == "for":
            self.agregarToken(TipoToken.RESERVADA_FOR, "for")
            if self.boolGrafo2:
                self.dotAFD2.node("6", label="E6", shape="doublecircle")
                self.dotAFD2.edge("0", "6", "for")
            return True
        elif self.lexemaTemp.lower() == "if":
            self.agregarToken(TipoToken.RESERVADA_IF, "if")
            if self.boolGrafo2:
                self.dotAFD2.node("6", label="E6", shape="doublecircle")
                self.dotAFD2.edge("0", "6", "if")
            return True
        elif self.lexemaTemp.lower() == "var":
            self.agregarToken(TipoToken.RESERVADA_VAR, "var")
            if self.boolGrafo2:
                self.dotAFD2.node("6", label="E6", shape="doublecircle")
                self.dotAFD2.edge("0", "6", "var")
            return True
        elif self.lexemaTemp.lower() == "math":
            self.agregarToken(TipoToken.RESERVADA_VAR, "Math")
            if self.boolGrafo2:
                self.dotAFD2.node("6", label="E6", shape="doublecircle")
                self.dotAFD2.edge("0", "6", "Math")
            return True
        elif self.lexemaTemp.lower() == "pow":
            self.agregarToken(TipoToken.RESERVADA_VAR, "pow")
            if self.boolGrafo2:
                self.dotAFD2.node("6", label="E6", shape="doublecircle")
                self.dotAFD2.edge("0", "6", "pow")
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


''''

'''
