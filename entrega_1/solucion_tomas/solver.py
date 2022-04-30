import numpy as np
from tree import tree


# bond and brach
def solver_tree(file_path):
    # f = open(file=file_path)
    # text = f.read()
    text = file_path  # eliminar y descomentar las anteriores
    lines = text.split('\n')
    # lines.remove('') #descoemntar tambien
    first_line = lines[0].split()
    n = int(first_line[0])
    K = int(first_line[1])

    lines = np.array([lines[i].split() for i in range(1, len(lines))]).astype(int)
    lines = np.append(lines, (lines[:, 0] / lines[:, 1]).reshape(-1, 1), axis=1)
    sorted_efficiencies = np.argsort(lines[:, 2])[::-1]
    lines = lines[sorted_efficiencies]

    de_sorted_efficiencies = np.argsort(sorted_efficiencies)

    initial_tree = tree(lista_valores=lines[:, 0], lista_pesos=lines[:, 1], capacidad=K, lista_decisiones=[], valor=0,
                        mejor_calculado=0, mejores_decisio=[])
    initial_tree.run()

    formated_mejores_decisiones = np.concatenate((np.array(initial_tree.mejores_decisio), np.zeros(n - len(
        initial_tree.mejores_decisio))))  # [de_sorted_efficiencies] # a las deciciones, le agrego los 0 que falten, concateno y despues ordeno
    formated_mejores_decisiones = formated_mejores_decisiones.astype(int).astype(str)
    solution = f'{int(initial_tree.mejor_calculado)} {1}\n{" ".join(formated_mejores_decisiones)}'  # '{" ".join(list(traceback_decition_x.astype(str)))}'

    # print(np.append(lines[:,:2][de_sorted_efficiencies].astype(int),formated_mejores_decisiones.astype(int).reshape(-1,1),axis=1))

    return solution
    return int(initial_tree.mejor_calculado), list(
        np.concatenate((np.array(initial_tree.mejores_decisio), np.zeros(n - len(initial_tree.mejores_decisio))))[
            de_sorted_efficiencies])
