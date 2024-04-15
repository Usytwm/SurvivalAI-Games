from typing import List, Dict, Set
from actions import Action, Attack, Action_Type
from scipy.cluster.hierarchy import DisjointSet

class Graph_of_Attacks:
    """Cada agente involucrado sera un nodo, y cada ataque una arista. Es un grafo dirigido.
    Edges, guarda las aristas como un diccionario que a cada agente, referenciado
    a traves de su id, le hace corresponder los ataques que realiza.
    Estos ataques a su vez aparecen como un diccionario donde a cada uno de los id de los
    agentes atacados, le hace corresponder la fuerza del ataque a tal agente.
    (O sea, para cada agente tenemos un diccionario con sus ataques, y en ese diccionario
    para cada agente atacado tenemos la fuerza del ataque realizado a ese agente)
    Esta clase tiene ademas un disjoint set que usamos para extraer los componentes conexos
    sin esfuerzo.
    """
    def __init__(self, actions_dict : Dict[int, List[Action]]):
        self.edges : Dict[int, Dict[int, int]] = {}
        self.djs = DisjointSet()

        for id, actions_list in actions_dict.items():
            attack_actions : List[Attack] = [act for act in actions_list if act.type.value == Action_Type.ATTACK.value]
            if len(attack_actions) > 0:
                if not id in self.edges:
                    self.edges[id] = {}
                    self.djs.add(id)
                for attack in attack_actions:
                    victim_id = attack.destinataries_ids[0]
                    if not victim_id in self.edges:
                        self.edges[victim_id] = {}
                        self.djs.add(victim_id)
                    self.edges[id][victim_id] = attack.strength
                    self.djs.merge(id, victim_id)
    
    @property
    def empty(self):
        return (len(self.djs) == 0)

    def connected_components(self) -> List['Component_of_Attacks_Graph']:
        connected_components = []
        for subset in self.djs.subsets():
            connected_components.append(Component_of_Attacks_Graph(self, subset))
        return connected_components

class Component_of_Attacks_Graph:
    def __init__(self, graph_of_attacks : Graph_of_Attacks, subset : List[int]):
        self.edges : Dict[int, Dict[int, Dict[int, int]]]= {}
        self.members = subset
        for id in subset:
            self.edges[id] = graph_of_attacks.edges[id]