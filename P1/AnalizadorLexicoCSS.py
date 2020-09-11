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

            if self.evaluarSimbolos():
                self.posicion += 1
                self.contadorH += 1
                caracterActual = self.entradaTexto[self.posicion]

            # Caracteres Dobles
            elif caracterActual == ":":
                self.estadoE12()

            # Estado E0 -> E1 -> E2 -> E3 -> E4
            elif caracterActual == "/":
                self.estadoE1()
            # Estado E0 -> E13
            elif caracterActual == "\"":
                self.estadoE13()
            # Estado E0 -> E8
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
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        caracter = self.entradaTexto[self.posicion]

        if caracter == "*":
            # Para el path del comentario
            if self.contadorComentario != 3:
                self.contadorComentario += 1
            # E1 -> E2
            self.lexemaTemp += caracter
            self.posicion += 1
            self.contadorH += 1
            self.estadoE2()

    def estadoE2(self):
        while self.posicion < (len(self.entradaTexto)-1):
            caracter = self.entradaTexto[self.posicion]

            if caracter == "*":
                # Estado E3
                self.lexemaTemp += caracter
                if self.entradaTexto[self.posicion + 1] == "/":
                    # Estado E4
                    self.lexemaTemp += self.entradaTexto[self.posicion + 1]
                    self.posicion += 2
                    self.contadorH += 2
                    self.agregarToken(TipoTokenCSS.COMENTARIO_MULTILINEA, self.lexemaTemp)
                    return
            else:
                self.lexemaTemp += caracter
                if caracter == "\n":
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
        self.agregarToken(TipoTokenCSS.COMENTARIO_MULTILINEA, self.lexemaTemp)
        print("No se detecto */")
        self.lexemaTemp = ""

    # -------------------- ID , #ID  ------------------------------------------
    def estadoE7(self):
        final = self.obtenerLongitud() + self.posicion
        print(final)
        for i in range(self.posicion, final):
            self.lexemaTemp += self.entradaTexto[i]
        # E0 -> E7
        if self.evaluarReservadas():
            self.contadorH += self.obtenerLongitud()
            self.posicion = final
            return

        self.estadoE8(final)

    def estadoE8(self, final):
        self.lexemaTemp = ""

        caracterActual = self.entradaTexto[self.posicion]

        if caracterActual == "#":
            if self.entradaTexto[self.posicion + 1].isalpha():
                self.lexemaTemp += caracterActual
                self.posicion += 1
                self.contadorH += 1
            else:
                self.agregarError(caracterActual, self.contadorH, self.contadorV)
                self.contadorH += 1
                self.posicion += 1
                return

        while self.posicion < final:
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
            if (self.posicion + 1) == final:
                if not self.evaluarReservadas():
                    self.agregarToken(TipoTokenCSS.ID, self.lexemaTemp)
            self.posicion += 1
            self.contadorH += 1

    # ----------------------     NUMEROS   ----------------------
    def estadoE9(self):
        final = self.obtenerLongitudNumero() + self.posicion
        while self.posicion < final:
            caracter = self.entradaTexto[self.posicion]
            if caracter.isnumeric():
                self.lexemaTemp += caracter
            else:
                self.agregarError(caracter, self.contadorH, self.contadorV)
                print(f"Error Lexico: {caracter}")

            if self.posicion + 1 == final:
                self.agregarToken(TipoTokenCSS.NUMERO_ENTERO, self.lexemaTemp)
            self.posicion += 1
            self.contadorH += 1
        self.posicion = final

    # ------------------ SIMBOLO : , ::   -------------------------------
    def estadoE12(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1

        caracter = self.entradaTexto[self.posicion]

        if caracter == ":":
            self.lexemaTemp += caracter
            self.agregarToken(TipoTokenCSS.SIMBOLO_DOBLE_DOS_PUNTOS, self.lexemaTemp)
        else:
            self.agregarToken(TipoTokenCSS.SIMBOLO_DOS_PUNTOS, self.lexemaTemp)
            self.posicion -= 1
            self.contadorH -= 1
        self.posicion += 1
        self.contadorH += 1

    # ------------------  CADENAS  -------------------------------
    def estadoE13(self):
        self.lexemaTemp += self.entradaTexto[self.posicion]
        self.posicion += 1
        self.contadorH += 1
        while self.entradaTexto[self.posicion] != "\n":
            caracterActual = self.entradaTexto[self.posicion]
            self.lexemaTemp += caracterActual
            if caracterActual == "\"":
                self.agregarToken(TipoTokenCSS.CADENA_TEXTO, self.lexemaTemp)
                self.posicion += 1
                self.contadorH += 1
                return
            self.contadorH += 1
            self.posicion += 1
        self.agregarToken(TipoTokenCSS.CADENA_TEXTO, self.lexemaTemp)

    # ------------------------------------  EVALUAR SIMBOLOS  ------------------------------------
    def evaluarSimbolos(self):
        caracterActual = self.entradaTexto[self.posicion]
        if caracterActual == ",":
            self.agregarToken(TipoTokenCSS.SIMBOLO_COMA, ",")
            return True
        elif caracterActual == ";":
            self.agregarToken(TipoTokenCSS.SIMBOLO_PUNTO_Y_COMA, ";")
            return True
        elif caracterActual == "{":
            self.agregarToken(TipoTokenCSS.SIMBOLO_LLAVES_ABRE, "{")
            return True
        elif caracterActual == "}":
            self.agregarToken(TipoTokenCSS.SIMBOLO_LLAVES_CIERRA, "}")
            return True
        elif caracterActual == "(":
            self.agregarToken(TipoTokenCSS.SIMBOLO_PARENTESIS_ABRE, "(")
            return True
        elif caracterActual == ")":
            self.agregarToken(TipoTokenCSS.SIMBOLO_PARENTESIS_CIERRA, ")")
            return True
        elif caracterActual == "*":
            self.agregarToken(TipoTokenCSS.SIGNO_MULTIPLICACION, "*")
            return True
        elif caracterActual == "-":
            self.agregarToken(TipoTokenCSS.SIGNO_MENOS, "-")
            return True
        elif caracterActual == "%":
            self.agregarToken(TipoTokenCSS.SIMBOLO_PORCENTAJE, "%")
            return True
        elif caracterActual == ".":
            self.agregarToken(TipoTokenCSS.SIMBOLO_PUNTO, ".")
            return True

    def evaluarReservadas(self):
        if self.lexemaTemp.lower() == "color":
            self.agregarToken(TipoTokenCSS.RESERVADA, "color")
            return True
        elif self.lexemaTemp.lower() == "background-color":
            self.agregarToken(TipoTokenCSS.RESERVADA, "background-color")
            return True

        elif self.lexemaTemp.lower() == "background-image":
            self.agregarToken(TipoTokenCSS.RESERVADA, "background-image")
            return True

        elif self.lexemaTemp.lower() == "border":
            self.agregarToken(TipoTokenCSS.RESERVADA, "border")
            return True

        elif self.lexemaTemp.lower() == "opacity":
            self.agregarToken(TipoTokenCSS.RESERVADA, "Opacity")
            return True

        elif self.lexemaTemp.lower() == "background":
            self.agregarToken(TipoTokenCSS.RESERVADA, "background")
            return True

        elif self.lexemaTemp.lower() == "text-align":
            self.agregarToken(TipoTokenCSS.RESERVADA, "text-align")
            return True

        elif self.lexemaTemp.lower() == "font-family":
            self.agregarToken(TipoTokenCSS.RESERVADA, "font-family")
            return True

        elif self.lexemaTemp.lower() == "font-style":
            self.agregarToken(TipoTokenCSS.RESERVADA, "font-style")
            return True

        elif self.lexemaTemp.lower() == "font-weight":
            self.agregarToken(TipoTokenCSS.RESERVADA, "font-weight")
            return True

        elif self.lexemaTemp.lower() == "font-size":
            self.agregarToken(TipoTokenCSS.RESERVADA, "font-size")
            return True

        elif self.lexemaTemp.lower() == "font":
            self.agregarToken(TipoTokenCSS.RESERVADA, "font")
            return True

        elif self.lexemaTemp.lower() == "padding-left":
            self.agregarToken(TipoTokenCSS.RESERVADA, "padding-left")
            return True

        elif self.lexemaTemp.lower() == "padding-right":
            self.agregarToken(TipoTokenCSS.RESERVADA, "padding-right")
            return True

        elif self.lexemaTemp.lower() == "padding-bottom":
            self.agregarToken(TipoTokenCSS.RESERVADA, "padding-bottom")
            return True

        elif self.lexemaTemp.lower() == "padding-top":
            self.agregarToken(TipoTokenCSS.RESERVADA, "padding-top")
            return True

        elif self.lexemaTemp.lower() == "padding":
            self.agregarToken(TipoTokenCSS.RESERVADA, "padding")
            return True

        elif self.lexemaTemp.lower() == "display":
            self.agregarToken(TipoTokenCSS.RESERVADA, "display")
            return True

        elif self.lexemaTemp.lower() == "line-height":
            self.agregarToken(TipoTokenCSS.RESERVADA, "line-height")
            return True

        elif self.lexemaTemp.lower() == "width":
            self.agregarToken(TipoTokenCSS.RESERVADA, "width")
            return True

        elif self.lexemaTemp.lower() == "height":
            self.agregarToken(TipoTokenCSS.RESERVADA, "height")
            return True

        elif self.lexemaTemp.lower() == "margin-top":
            self.agregarToken(TipoTokenCSS.RESERVADA, "margin-top")
            return True

        elif self.lexemaTemp.lower() == "margin-right":
            self.agregarToken(TipoTokenCSS.RESERVADA, "margin-right")
            return True

        elif self.lexemaTemp.lower() == "margin-bottom":
            self.agregarToken(TipoTokenCSS.RESERVADA, "margin-bottom")
            return True

        elif self.lexemaTemp.lower() == "margin-left":
            self.agregarToken(TipoTokenCSS.RESERVADA, "margin-left")
            return True

        elif self.lexemaTemp.lower() == "margin":
            self.agregarToken(TipoTokenCSS.RESERVADA, "margin")
            return True

        elif self.lexemaTemp.lower() == "border-style":
            self.agregarToken(TipoTokenCSS.RESERVADA, "border-style")
            return True

        elif self.lexemaTemp.lower() == "display":
            self.agregarToken(TipoTokenCSS.RESERVADA, "display")
            return True

        elif self.lexemaTemp.lower() == "position":
            self.agregarToken(TipoTokenCSS.RESERVADA, "position")
            return True

        elif self.lexemaTemp.lower() == "bottom":
            self.agregarToken(TipoTokenCSS.RESERVADA, "bottom")
            return True

        elif self.lexemaTemp.lower() == "top":
            self.agregarToken(TipoTokenCSS.RESERVADA, "top")
            return True

        elif self.lexemaTemp.lower() == "right":
            self.agregarToken(TipoTokenCSS.RESERVADA, "right")
            return True

        elif self.lexemaTemp.lower() == "left":
            self.agregarToken(TipoTokenCSS.RESERVADA, "left")
            return True

        elif self.lexemaTemp.lower() == "float":
            self.agregarToken(TipoTokenCSS.RESERVADA, "float")
            return True

        elif self.lexemaTemp.lower() == "clear":
            self.agregarToken(TipoTokenCSS.RESERVADA, "clear")
            return True

        elif self.lexemaTemp.lower() == "max-width":
            self.agregarToken(TipoTokenCSS.RESERVADA, "max-width")
            return True

        elif self.lexemaTemp.lower() == "min-width":
            self.agregarToken(TipoTokenCSS.RESERVADA, "min-width")
            return True

        elif self.lexemaTemp.lower() == "max-height":
            self.agregarToken(TipoTokenCSS.RESERVADA, "max-height")
            return True

        elif self.lexemaTemp.lower() == "min-height":
            self.agregarToken(TipoTokenCSS.RESERVADA, "min-height")
            return True

        elif self.lexemaTemp.lower() == "px":
            self.agregarToken(TipoTokenCSS.MEDIDA, "px")
            return True

        elif self.lexemaTemp.lower() == "em":
            self.agregarToken(TipoTokenCSS.MEDIDA, "em")
            return True

        elif self.lexemaTemp.lower() == "vh":
            self.agregarToken(TipoTokenCSS.MEDIDA, "vh")
            return True

        elif self.lexemaTemp.lower() == "vw":
            self.agregarToken(TipoTokenCSS.MEDIDA, "vw")
            return True

        elif self.lexemaTemp.lower() == "in":
            self.agregarToken(TipoTokenCSS.MEDIDA, "in")
            return True

        elif self.lexemaTemp.lower() == "cm":
            self.agregarToken(TipoTokenCSS.MEDIDA, "cm")
            return True

        elif self.lexemaTemp.lower() == "mm":
            self.agregarToken(TipoTokenCSS.MEDIDA, "mm")
            return True

        elif self.lexemaTemp.lower() == "pt":
            self.agregarToken(TipoTokenCSS.MEDIDA, "pt")
            return True

        elif self.lexemaTemp.lower() == "pc":
            self.agregarToken(TipoTokenCSS.MEDIDA, "pc")
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
