from Token import TipoTokenCSS
from Token import Token
from ErrorLexico import ErrorLexico
from Posicion import Posicion


class AnalizadorLexicoCSS:
    def __init__(self):
        self.lista_Tokens = list()
        self.lista_ErroresLexicos = list()
        self.entradaTexto = ""
        self.lexemaTemp = ""
        self.textoCorregido = ""
        self.pathSalida = ""
        self.contadorV = 1
        self.contadorH = 1
        self.contadorComentario = 0
        self.posicion = 0
        self.bitacoraCSS = ""

    def agregarToken(self, tipoToken, lexemaValor):
        self.lista_Tokens.append(Token(tipoToken, lexemaValor))
        self.textoCorregido += lexemaValor
        self.lexemaTemp = ""

    def agregarTokenNinguno(self, tipoToken, lexemaValor):
        self.lista_Tokens.append(Token(tipoToken, lexemaValor))

    def agregarError(self, valor, posicionColumna, posicionFila):
        self.lista_ErroresLexicos.append(ErrorLexico(valor, Posicion(posicionColumna, posicionFila)))

    def ScannerCSS(self, entrada):
        self.entradaTexto = f"{entrada}#"
        self.posicion = 0

        while self.posicion < (len(self.entradaTexto)):

            caracterActual = self.entradaTexto[self.posicion]

            # E0 -> E14 (, , : , ;)
            if self.evaluarSimbolos():
                self.posicion += 1
                self.contadorH += 1
                caracterActual = self.entradaTexto[self.posicion]

            # Caracteres Dobles
            # E0 -> E12 (:)
            elif caracterActual == ":":
                self.estadoE12()

            # Estado E0 -> E1 -> E2 -> E3 -> E4
            elif caracterActual == "/":
                self.estadoE1()
            # Estado E0 -> E13
            elif caracterActual == "\"":
                self.estadoE13()
            # Estado E0 -> E7
            elif caracterActual == "#" and self.posicion != (len(self.entradaTexto) - 1):
                self.estadoE7()
            # Estado E0 -> E7 -> E5
            elif caracterActual.isalpha():
                self.estadoE7()
            elif caracterActual.isnumeric():
                self.estadoE9()

            elif caracterActual == " " or caracterActual == "\t" or caracterActual == "\n":
                if caracterActual == "\n":
                    self.contadorV += 1
                    self.contadorH = 1
                else:
                    self.contadorH += 1
                self.textoCorregido += caracterActual
                self.agregarTokenNinguno(TipoTokenCSS.NINGUNO, caracterActual)
                self.posicion += 1
                continue
            else:
                if (caracterActual == "#") and (self.posicion == (len(self.entradaTexto) - 1)):
                    print("analisis CSS finalizado")
                    print(f"Posicion Cursor (H, V): {self.contadorH}, {self.contadorV}")
                else:
                    print(f"Error Lexico. {caracterActual}")
                    self.agregarError(caracterActual, self.contadorH, self.contadorV)
                self.contadorH += 1
                self.posicion += 1
        return self.lista_Tokens

    # --------------   COMENTARIOS   --------------
    def estadoE1(self):
        self.bitacoraCSS += f"[I: E0]->[F: E1] C: /\n"
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        caracter = self.entradaTexto[self.posicion]

        if caracter == "*":
            self.bitacoraCSS += "[I: E1]->[F: E2] C: *\n"
            # Para el path del comentario
            if self.contadorComentario != 3:
                self.contadorComentario += 1
            # E1 -> E2
            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            self.estadoE2()
        else:
            self.bitacoraCSS += "\nERROR: E1 C: /\n"
            self.agregarError(self.lexemaTemp, self.contadorH-1, self.contadorV)
            self.lexemaTemp = ""

    def estadoE2(self):
        while self.posicion < (len(self.entradaTexto)-1):
            caracter = self.entradaTexto[self.posicion]

            if caracter == "*":
                # Estado E2 -> E3
                self.lexemaTemp += caracter
                self.bitacoraCSS += "[I: E2]->[F: E3] C: *\n"
                if self.entradaTexto[self.posicion + 1] == "/":
                    # Estado E3 -> E4
                    self.lexemaTemp += self.entradaTexto[self.posicion + 1]
                    self.bitacoraCSS += f"[I: E3]->[F: E4] C: {self.entradaTexto[self.posicion+1]}\n"
                    self.posicion += 2
                    self.contadorH += 2
                    self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.COMENTARIO_MULTILINEA.name}\n\n"
                    self.agregarToken(TipoTokenCSS.COMENTARIO_MULTILINEA, self.lexemaTemp)
                    return
                # E3 -> E2
            else:
                # E2 -> E2
                self.bitacoraCSS += f"[I: E2]->[F: E2] C: {caracter} \n"
                self.lexemaTemp += caracter
                if caracter == "\n":
                    self.contadorH = 1
                    self.contadorV += 1

            if caracter == "C" and self.contadorComentario == 2:
                self.contadorComentario += 1
                contadorPath = self.posicion
                while self.entradaTexto[contadorPath] != "*":
                    self.pathSalida += self.entradaTexto[contadorPath]
                    contadorPath += 1

            self.posicion += 1
            self.contadorH += 1
        self.posicion -= 1
        self.contadorH -= 1
        self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.COMENTARIO_MULTILINEA.name}\n\n"
        self.agregarToken(TipoTokenCSS.COMENTARIO_MULTILINEA, self.lexemaTemp)
        print("No se detecto */")
        self.lexemaTemp = ""

    # -------------------- ID , #ID  ------------------------------------------
    # E0 -> E7
    def estadoE7(self):
        final = self.obtenerLongitud() + self.posicion
        for i in range(self.posicion, final):
            self.lexemaTemp += self.entradaTexto[i]
        # E0 -> E7
        if self.evaluarReservadas():
            self.contadorH += self.obtenerLongitud()
            self.posicion = final
            return

        self.estadoE8(final)

    # E0 -> E8   o  E7 -> E8
    def estadoE8(self, final):
        self.lexemaTemp = ""

        caracterActual = self.entradaTexto[self.posicion]

        if caracterActual == "#":
            # E8
            if self.entradaTexto[self.posicion + 1].isalpha() or self.entradaTexto[self.posicion + 1].isnumeric():
                self.bitacoraCSS += "[I: E0]->[F: E8] C: #\n"
                self.lexemaTemp += caracterActual
                self.posicion += 1
                self.contadorH += 1
            else:
                self.bitacoraCSS += "[ERROR E8] C: #\n"
                self.agregarError(caracterActual, self.contadorH, self.contadorV)
                self.contadorH += 1
                self.posicion += 1
                return

        self.bitacoraCSS += f"[I: E8]->[F: E5] C: {self.entradaTexto[self.posicion]}\n"
        while self.posicion < final:
            # E5
            caracterActual = self.entradaTexto[self.posicion]

            if caracterActual.isalpha():
                self.lexemaTemp += caracterActual
            elif caracterActual.isnumeric():
                self.lexemaTemp += caracterActual
            elif caracterActual == "-":
                self.lexemaTemp += caracterActual
            elif caracterActual == "#":
                self.lexemaTemp += caracterActual
            else:
                self.agregarError(caracterActual, self.contadorH, self.contadorV)
                print(f"Error Lexico: {caracterActual}")
                self.bitacoraCSS += f"[ERROR E5] C: {caracterActual}\n"

            if (self.posicion + 1) == final:
                if not self.evaluarReservadas():
                    self.agregarToken(TipoTokenCSS.ID, self.lexemaTemp)
                    self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.ID.name}\n\n"
            if (self.posicion + 1) != final:
                self.bitacoraCSS += f"[I: E5]->[F: E5] C: {self.entradaTexto[self.posicion + 1]}\n"
            self.posicion += 1
            self.contadorH += 1

    # ----------------------     NUMEROS   ----------------------
    # E0 -> E9
    def estadoE9(self):
        final = self.obtenerLongitudNumero() + self.posicion
        self.bitacoraCSS += f"[I: E0]->[F: E9] C: {self.entradaTexto[self.posicion]}\n"
        while self.posicion < final:
            # E9 -> E9
            caracter = self.entradaTexto[self.posicion]
            if caracter.isnumeric():
                self.lexemaTemp += caracter
            else:
                self.agregarError(caracter, self.contadorH, self.contadorV)
                self.bitacoraCSS += f"\n[ERROR E9] C: {caracter}\n\n"
                print(f"Error Lexico: {caracter}")

            if self.posicion + 1 == final:
                self.agregarToken(TipoTokenCSS.NUMERO_ENTERO, self.lexemaTemp)
                self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.NUMERO_ENTERO.name}\n\n"

            if self.posicion + 1 != final:
                self.bitacoraCSS += f"[I: E9]->[F: E9] C: {caracter}\n"

            self.posicion += 1
            self.contadorH += 1
        self.posicion = final

    # ------------------ SIMBOLO : , ::   -------------------------------
    def estadoE12(self):
        self.bitacoraCSS += "[I: E0]->[F: E12] C: :\n"
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1

        caracter = self.entradaTexto[self.posicion]

        # E12 -> E15 (::)
        if caracter == ":":
            self.bitacoraCSS += "[I: E12]->[F: E15] C: ::\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.SIMBOLO_DOBLE_DOS_PUNTOS.name}\n\n"
            self.lexemaTemp += caracter
            self.agregarToken(TipoTokenCSS.SIMBOLO_DOBLE_DOS_PUNTOS, self.lexemaTemp)
        else:
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.SIMBOLO_DOS_PUNTOS.name}\n\n"
            self.agregarToken(TipoTokenCSS.SIMBOLO_DOS_PUNTOS, self.lexemaTemp)
            self.posicion -= 1
            self.contadorH -= 1
        self.posicion += 1
        self.contadorH += 1

    # ------------------  CADENAS  -------------------------------
    # E0->E13
    def estadoE13(self):
        self.bitacoraCSS += "[I: E0]->[F: E13] C: \" \n"
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        while self.entradaTexto[self.posicion] != "\n":
            # E13 -> E13
            caracterActual = self.entradaTexto[self.posicion]
            self.lexemaTemp += caracterActual
            if caracterActual == "\"":
                # E13 -> E16
                self.bitacoraCSS += "[I: E13]->[F: E:16] C: \" \n"
                self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.CADENA_TEXTO.name}\n\n"
                self.agregarToken(TipoTokenCSS.CADENA_TEXTO, self.lexemaTemp)
                self.posicion += 1
                self.contadorH += 1
                return
            self.bitacoraCSS += f"[I: E13]->[F: E113] C: {caracterActual}\n"
            self.contadorH += 1
            self.posicion += 1
        # E13 -> E16
        self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.CADENA_TEXTO.name}\n\n"
        self.agregarToken(TipoTokenCSS.CADENA_TEXTO, self.lexemaTemp)

    # ------------------------------------  EVALUAR SIMBOLOS  ------------------------------------
    # E0 -> E14
    def evaluarSimbolos(self):
        caracterActual = self.entradaTexto[self.posicion]
        if caracterActual == ",":
            self.agregarToken(TipoTokenCSS.SIMBOLO_COMA, ",")
            self.bitacoraCSS += f"[I: E0] -> [F: E14] C: ,\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.SIMBOLO_COMA.name}\n\n"
            return True
        elif caracterActual == ";":
            self.agregarToken(TipoTokenCSS.SIMBOLO_PUNTO_Y_COMA, ";")
            self.bitacoraCSS += f"[I: E0]->[F: E14] C: ;\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.SIMBOLO_PUNTO_Y_COMA.name}\n\n"
            return True
        elif caracterActual == "{":
            self.agregarToken(TipoTokenCSS.SIMBOLO_LLAVES_ABRE, "{")
            self.bitacoraCSS += "[I: E0]->[F: E14] C: {\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.SIMBOLO_LLAVES_ABRE.name}\n\n"
            return True
        elif caracterActual == "}":
            self.agregarToken(TipoTokenCSS.SIMBOLO_LLAVES_CIERRA, "}")
            self.bitacoraCSS += "[I: E0]->[F: E14] C: }\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.SIMBOLO_LLAVES_CIERRA.name}\n\n"
            return True
        elif caracterActual == "(":
            self.agregarToken(TipoTokenCSS.SIMBOLO_PARENTESIS_ABRE, "(")
            self.bitacoraCSS += "[I: E0]->[F: E14] C: (\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.SIMBOLO_PARENTESIS_ABRE.name}\n\n"
            return True
        elif caracterActual == ")":
            self.agregarToken(TipoTokenCSS.SIMBOLO_PARENTESIS_CIERRA, ")")
            self.bitacoraCSS += "[I: E0]->[F: E14] C: (\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.SIMBOLO_PARENTESIS_CIERRA.name}\n\n"
            return True
        elif caracterActual == "*":
            self.agregarToken(TipoTokenCSS.SIGNO_MULTIPLICACION, "*")
            self.bitacoraCSS += "[I: E0]->[F: E14] C: *\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.SIGNO_MULTIPLICACION.name}\n\n"
            return True
        elif caracterActual == "-":
            self.agregarToken(TipoTokenCSS.SIGNO_MENOS, "-")
            self.bitacoraCSS += "[I: E0]->[F: E14] C: -\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.SIGNO_MENOS.name}\n\n"
            return True
        elif caracterActual == "%":
            self.agregarToken(TipoTokenCSS.SIMBOLO_PORCENTAJE, "%")
            self.bitacoraCSS += "[I: E0]->[F: E14] C: %\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.SIMBOLO_PORCENTAJE.name}\n\n"
            return True
        elif caracterActual == ".":
            self.agregarToken(TipoTokenCSS.SIMBOLO_PUNTO, ".")
            self.bitacoraCSS += "[I: E0]->[F: E14] C: .\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.SIMBOLO_PUNTO.name}\n\n"
            return True

    def evaluarReservadas(self):
        if self.lexemaTemp.lower() == "color":
            self.agregarToken(TipoTokenCSS.RESERVADA, "color")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: color\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True
        elif self.lexemaTemp.lower() == "background-color":
            self.agregarToken(TipoTokenCSS.RESERVADA, "background-color")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: background-color\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "background-image":
            self.agregarToken(TipoTokenCSS.RESERVADA, "background-image")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: background-image\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "border":
            self.agregarToken(TipoTokenCSS.RESERVADA, "border")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: border\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "opacity":
            self.agregarToken(TipoTokenCSS.RESERVADA, "Opacity")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: Opacity\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "background":
            self.agregarToken(TipoTokenCSS.RESERVADA, "background")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: background\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "text-align":
            self.agregarToken(TipoTokenCSS.RESERVADA, "text-align")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: text-align\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "font-family":
            self.agregarToken(TipoTokenCSS.RESERVADA, "font-family")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: font-family\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "font-style":
            self.agregarToken(TipoTokenCSS.RESERVADA, "font-style")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: font-style\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "font-weight":
            self.agregarToken(TipoTokenCSS.RESERVADA, "font-weight")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: font-weight\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "font-size":
            self.bitacoraCSS += "[I: E0]->[F: E7] C: font-size\n"
            self.agregarToken(TipoTokenCSS.RESERVADA, "font-size")
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "font":
            self.agregarToken(TipoTokenCSS.RESERVADA, "font")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: font\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "padding-left":
            self.agregarToken(TipoTokenCSS.RESERVADA, "padding-left")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: padding-left\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "padding-right":
            self.agregarToken(TipoTokenCSS.RESERVADA, "padding-right")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: padding-right\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "padding-bottom":
            self.agregarToken(TipoTokenCSS.RESERVADA, "padding-bottom")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: padding-bottom\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "padding-top":
            self.bitacoraCSS += "[I: E0]->[F: E7] C: padding-top\n"
            self.agregarToken(TipoTokenCSS.RESERVADA, "padding-top")
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "padding":
            self.agregarToken(TipoTokenCSS.RESERVADA, "padding")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: padding\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "display":
            self.agregarToken(TipoTokenCSS.RESERVADA, "display")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: display\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "line-height":
            self.agregarToken(TipoTokenCSS.RESERVADA, "line-height")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: line-height\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "width":
            self.agregarToken(TipoTokenCSS.RESERVADA, "width")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: width\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "height":
            self.agregarToken(TipoTokenCSS.RESERVADA, "height")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: height\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "margin-top":
            self.agregarToken(TipoTokenCSS.RESERVADA, "margin-top")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: margin-top\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "margin-right":
            self.agregarToken(TipoTokenCSS.RESERVADA, "margin-right")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: margin-right\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "margin-bottom":
            self.agregarToken(TipoTokenCSS.RESERVADA, "margin-bottom")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: margin-bottom\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "margin-left":
            self.agregarToken(TipoTokenCSS.RESERVADA, "margin-left")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: margin-left\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "margin":
            self.agregarToken(TipoTokenCSS.RESERVADA, "margin")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: margin\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "border-style":
            self.agregarToken(TipoTokenCSS.RESERVADA, "border-style")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: border-style\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "display":
            self.agregarToken(TipoTokenCSS.RESERVADA, "display")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: display\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "position":
            self.agregarToken(TipoTokenCSS.RESERVADA, "position")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: position\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "bottom":
            self.agregarToken(TipoTokenCSS.RESERVADA, "bottom")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: bottom\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "top":
            self.agregarToken(TipoTokenCSS.RESERVADA, "top")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: top\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "right":
            self.agregarToken(TipoTokenCSS.RESERVADA, "right")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: right\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "left":
            self.agregarToken(TipoTokenCSS.RESERVADA, "left")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: left\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "float":
            self.agregarToken(TipoTokenCSS.RESERVADA, "float")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: float\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "clear":
            self.agregarToken(TipoTokenCSS.RESERVADA, "clear")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: clear\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "max-width":
            self.agregarToken(TipoTokenCSS.RESERVADA, "max-width")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: max-width\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "min-width":
            self.agregarToken(TipoTokenCSS.RESERVADA, "min-width")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: min-width\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "max-height":
            self.agregarToken(TipoTokenCSS.RESERVADA, "max-height")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: max-height\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "min-height":
            self.agregarToken(TipoTokenCSS.RESERVADA, "min-height")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: min-height\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "px":
            self.agregarToken(TipoTokenCSS.MEDIDA, "px")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: px\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "em":
            self.agregarToken(TipoTokenCSS.MEDIDA, "em")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: em\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "vh":
            self.agregarToken(TipoTokenCSS.MEDIDA, "vh")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: vh\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "vw":
            self.agregarToken(TipoTokenCSS.MEDIDA, "vw")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: vw\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "in":
            self.agregarToken(TipoTokenCSS.MEDIDA, "in")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: in\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "cm":
            self.agregarToken(TipoTokenCSS.MEDIDA, "cm")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: cm\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "mm":
            self.agregarToken(TipoTokenCSS.MEDIDA, "mm")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: mm\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "pt":
            self.agregarToken(TipoTokenCSS.MEDIDA, "pt")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: pt\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

        elif self.lexemaTemp.lower() == "pc":
            self.agregarToken(TipoTokenCSS.MEDIDA, "pc")
            self.bitacoraCSS += "[I: E0]->[F: E7] C: pc\n"
            self.bitacoraCSS += f"\n[TOKEN RECONOCIDO] {TipoTokenCSS.RESERVADA.name}\n\n"
            return True

    def obtenerLongitud(self):
        contador = 0
        for i in range(self.posicion, len(self.entradaTexto) - 1):
            if self.entradaTexto[i] == " " or self.entradaTexto[i] == "\t" or self.entradaTexto[i] == "\n" \
                    or self.entradaTexto[i] == "\r" or self.entradaTexto[i] == "{" or self.entradaTexto[i] == "}" \
                    or self.entradaTexto[i] == "(" or self.entradaTexto[i] == ")" or self.entradaTexto[i] == ";" \
                    or self.entradaTexto[i] == "," or self.entradaTexto[i] == ":" or self.entradaTexto[i] == "." \
                    or self.entradaTexto[i] == "*" or self.entradaTexto[i] == "%":
                break
            contador += 1
        return contador

    def obtenerLongitudNumero(self):
        contador = 0
        for i in range(self.posicion, len(self.entradaTexto) - 1):
            if self.entradaTexto[i] == " " or self.entradaTexto[i] == "\t" or self.entradaTexto[i] == "\n" \
                    or self.entradaTexto[i] == "\r" or self.entradaTexto[i] == "{" or self.entradaTexto[i] == "}" \
                    or self.entradaTexto[i] == "(" or self.entradaTexto[i] == ")" or self.entradaTexto[i] == ";" \
                    or self.entradaTexto[i] == "," or self.entradaTexto[i] == ":" or self.entradaTexto[i] == "." or \
                    self.entradaTexto[i].isalpha() or self.entradaTexto[i] == "%":
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
