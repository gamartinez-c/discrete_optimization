from node import node

class tree():
    def __init__(self, lista_valores, lista_pesos, capacidad, ):
        self.lista_valores = lista_valores
        self.lista_pesos = lista_pesos
        self.capacidad = capacidad
        self.mejor_nodo = None
        self.node_inicial = None
        self.edge_node_list = []

    def run(self):
        self.node_inicial.run()
