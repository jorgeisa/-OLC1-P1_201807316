from enum import Enum


class TipoToken(Enum):
    # Palabras Reservadas
    RESERVADA_RETURN = 1
    RESERVADA_BREAK = 2
    RESERVADA_CONTINUE = 3
    RESERVADA_DO = 4
    RESERVADA_WHILE = 5
    RESERVADA_FOR = 6
    RESERVADA_IF = 7
    RESERVADA_VAR = 8

    # Simbolos
    SIMBOLO_LLAVE_ABRE = 9
    SIMBOLO_LLAVE_CIERRA = 10
    SIMBOLO_PARENTESIS_ABRE = 11
    SIMBOLO_PARENTESIS_CIERRA = 12
    SIMBOLO_PUNTO_COMA = 13
    SIMBOLO_COMA = 14
    SIMBOLO_IGUAL = 15
    SIMBOLO_MENOR_QUE = 16
    SIMBOLO_MAYOR_QUE = 17
    SIMBOLO_MENOR_IGUAL = 18
    SIMBOLO_MAYOR_IGUAL = 19
    SIMBOLO_NO_IGUAL = 20
    SIMBOLO_IGUAL_COMPARATIVO = 21
    SIMBOLO_DOS_PUNTOS = 22

    # Signo
    SIGNO_MAS = 23
    SIGNO_MENOS = 24
    SIGNO_MULTIPLICACION = 25
    SIGNO_RESTA = 26

    # Expresiones Regulares
    ID = 50
    NUMERO_ENTERO = 51
    COMENTARIO_UNILINEA = 52
    COMENTARIO_MULTILINEA = 53
    DESCONOCIDO = 54
    NINGUNO = 55

    def describe(self):
        return self.value


class Token:

    def __init__(self, tipoToken, lexemaValor):
        self.tipoToken = tipoToken
        self.lexemaValor = lexemaValor

    def getValor(self):
        return self.lexemaValor

    def getTipoToken(self):
        return self.tipoToken
