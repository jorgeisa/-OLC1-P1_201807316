class ErrorLexico():
    def __init__(self, valor, posicion):
        self.valor = valor
        self.posicion = posicion

    def getPosicion(self):
        return self.posicion

    def setPosicion(self, posicion):
        self.posicion = posicion

    def getValor(self):
        return self.valor
