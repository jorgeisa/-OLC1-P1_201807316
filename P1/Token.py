from enum import Enum
from Posicion import Posicion


class TipoToken(Enum):
    # Palabras Reservadas
    RESERVADA_RETURN = 1  #
    RESERVADA_BREAK = 2  #
    RESERVADA_CONTINUE = 3  #
    RESERVADA_DO = 4  #
    RESERVADA_WHILE = 5  #
    RESERVADA_FOR = 6  #
    RESERVADA_IF = 7  #
    RESERVADA_VAR = 8  #
    RESERVADA_ELSE = 9  #
    RESERVADA_THIS = 10  #
    RESERVADA_CLASS = 11  #
    RESERVADA_CONSOLE = 12  #
    RESERVADA_LOG = 13  #
    RESERVADA_FALSE = 14
    RESERVADA_TRUE = 15
    RESERVADA_CONSTRUCTOR = 16
    RESERVADA_FUNCTION = 17
    RESERVADA_MATH = 18
    RESERVADA_POW = 19

    # Simbolos
    # = , > , < , { , }, (, ), . , ; , , , !, :
    SIMBOLO_IGUAL = 100
    SIMBOLO_MAYOR_QUE = 101
    SIMBOLO_MENOR_QUE = 102
    SIMBOLO_LLAVE_ABRE = 103
    SIMBOLO_LLAVE_CIERRA = 104
    SIMBOLO_PARENTESIS_ABRE = 105
    SIMBOLO_PARENTESIS_CIERRA = 106
    SIMBOLO_PUNTO = 107
    SIMBOLO_PUNTO_COMA = 108
    SIMBOLO_COMA = 109
    SIMBOLO_NEGACION = 110
    SIMBOLO_DOS_PUNTOS = 111

    # Relacionales == , != , >= , <=
    RELACIONAL_IGUAL = 112
    RELACIONAL_DISTINTO = 113
    RELACIONAL_MAYOR_IGUAL = 114
    RELACIONAL_MENOR_IGUAL = 115

    # +=, ++, ===, =>, *=
    SIMBOLO_ASIGNACION_ADICION = 116
    SIMBOLO_INCREMENTO = 117
    SIMBOLO_ESTRICTAMENTE_IGUALES = 118
    SIMBOLO_LAMBDA = 119
    SIMBOLO_ASIGNACION_MULTIPLICACION = 120

    # Logico
    # &&, ||
    LOGICO_CONJUNCION = 121
    LOGICO_DISYUNCION = 122

    # Signo
    # + , -, *, /
    SIGNO_SUMA = 200
    SIGNO_RESTA = 201
    SIGNO_MULTIPLICACION = 202
    SIGNO_DIVISION = 203  # /

    # Expresiones Regulares
    ID = 300
    NUMERO_ENTERO = 301
    COMENTARIO_UNILINEA = 302
    COMENTARIO_MULTILINEA = 303
    CADENA_SIMPLES = 304
    CADENA_DOBLES = 305
    NINGUNO = 351

    def describe(self):
        return self.value


class TipoTokenCSS(Enum):
    # Reservadas
    RESERVADA = 1

    # Simbolos
    SIMBOLO_DOS_PUNTOS = 100
    SIMBOLO_DOBLE_DOS_PUNTOS = 101
    SIMBOLO_PUNTO = 102
    SIMBOLO_NUMERAL = 103
    SIMBOLO_PUNTO_Y_COMA = 104
    SIMBOLO_COMA = 105
    SIMBOLO_PARENTESIS_ABRE = 106
    SIMBOLO_PARENTESIS_CIERRA = 107
    SIMBOLO_LLAVES_ABRE = 108
    SIMBOLO_LLAVES_CIERRA = 109
    SIMBOLO_PORCENTAJE = 110

    # Signos
    SIGNO_MULTIPLICACION = 200
    SIGNO_MENOS = 201

    # Expresiones Regulares
    COMENTARIO_MULTILINEA = 300
    ID = 301
    CADENA_TEXTO = 302
    NUMERO_ENTERO = 303
    NINGUNO = 401

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
