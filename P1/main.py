from graphviz import Digraph
from PantallaPrincipal import PantallaPrincipal
import os

iniciar = PantallaPrincipal()

# Para el grafo de JS se tomo en cuenta lo siguiente
# Grafo 1 = Primera Cadena
# Grafo 2 = Primer ID
# Grafo 3 = Primer Comentario MULTILINEA


# Ejemplo pagina
# dot = Digraph(comment='The Round Table', format='jpg')
# dot.node('A', 'King Arthur')
# dot.node('B', 'Sir Bedevere')
# dot.node('L', 'Sir Lancelot')
#
# dot.edges(['AB', 'AL'])
# dot.edge('B', 'L', constraint='false')
# dot.render(filename="dot")

# Realizado
# dotArbol = Digraph(comment=f"nombre1Arbol", format='jpg')
# dotArbol.attr(rankdir='LR')
# dotArbol.node(f"1", label=f"jsjs", shape="circle")
# dotArbol.node(f"2", label=f"juju", shape="doublecircle", width="2")
# dotArbol.edge(f"1", "1", "enlace", dir="forward",)
# dotArbol.edge(f"1", "1", "Hola", dir="forward")
# dotArbol.edge(f"1", "2", "j")
# dotArbol.render(filename=f"nombreArbolxd")
