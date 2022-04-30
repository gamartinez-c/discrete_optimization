class node():
    def __init__(self, lista_valores, lista_pesos, capacidad, valor, lista_decisiones):
        self.lista_valores = lista_valores
        self.lista_pesos = lista_pesos
        self.capacidad = capacidad
        self.valor = valor
        self.tree = None
        self.nodo_1 = None
        self.nodo_0 = None
        self.nodo_valido = True
        self.lista_decisiones = lista_decisiones.copy()

    def update_value(self):
        if self.agrego & (self.lista_pesos[0] > self.capacidad):
            self.valor = -1
            self.capacidad = self.capacidad - self.lista_pesos[0]
            self.estimacion = -1
            self.nodo_valido = False
            self.lista_decisiones.append(-1)

        if self.agrego & self.nodo_valido:
            self.estimacion = self.valor + self.lista_valores[0] + self.relaxed_best()
            self.valor += self.lista_valores[0]
            self.lista_decisiones.append(1)
            self.capacidad = self.capacidad - self.lista_pesos[0]

        elif ~self.agrego & self.nodo_valido:
            self.estimacion = self.valor + self.relaxed_best()
            self.lista_decisiones.append(0)

    def get_relaxed_value(self):
        potential_value = 0
        current_capacity = self.capacidad
        list_of_weights = self.lista_pesos.copy()
        list_of_values = self.lista_valores.copy()
        can_i_add_portion_of_item = current_capacity > 0
        while can_i_add_portion_of_item:
            fraction_to_add = 1 if list_of_weights[0] < current_capacity else current_capacity/list_of_weights[0]
            potential_value += list_of_values[0] * fraction_to_add
            current_capacity -= list_of_weights[0] * fraction_to_add

            list_of_weights = list_of_weights[1:]
            list_of_values = list_of_values[1:]
            can_i_add_portion_of_item = current_capacity > 0

        return potential_value + self.valor

    def run(self):
        item_over_decision_value = self.lista_valores[0]
        item_over_decision_pesos = self.lista_pesos[0]

        if self in self.tree.edge_node_list:
            self.tree.edge_node_list.remove(self)

        self.nodo_0 = node(self.lista_valores[1:], self.lista_pesos[1:], self.capacidad, self.valor, self.lista_decisiones)
        self.tree.edge_node_list.append(self.nodo_0)
        if self.lista_pesos[0] < self.capacidad:
            self.nodo_1 = node(self.lista_valores[1:], self.lista_pesos[1:], self.capacidad - item_over_decision_pesos, self.valor + item_over_decision_value, self.lista_decisiones)
            self.tree.edge_node_list.append(self.nodo_1)

        best_node = self.tree.edge_node_list[0]
        for edge_node in self.tree.edge_node_list:
            if edge_node.get_relaxed_value() > best_node.get_relaxed_value():
                best_node = edge_node

        if len(best_node.lista_valores) != 0:
            best_node.run()
        else:
            self.tree.mejor_nodo = best_node
            print('Finish.')

    def relaxed_best(self):
        lista_valores = self.lista_valores[1:]
        lista_pesos = self.lista_pesos[1:]
        k = self.capacidad
        value = 0
        for i in range(len(lista_pesos)):
            if lista_pesos[i] < k:
                k -= lista_pesos[i]
                value += lista_valores[i]
            else:
                fraction = k / lista_pesos[i]
                value += fraction * lista_valores[i]

        return value

    def debugging_print(self):
        print('node calculation no: c:', self.nodo_0.capacidad,
              'v:', self.nodo_0.valor,
              '\tMejor', self.tree.mejor_nodo,
              '\tEstimado:', self.nodo_0.estimacion,
              '\tLista_valores', self.nodo_0.lista_valores,
              '\t', self.nodo_0.lista_decisiones)
