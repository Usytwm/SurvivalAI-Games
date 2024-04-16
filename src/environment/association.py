from typing import List, Tuple, Dict, Set
class Association:
    def __init__(self, id : int, members : Set[int], commitments : Dict[int, Tuple[int, int]]):
        """Una asociacion tiene un identificador, un conjunto con los ids de los agentes miembros
        y un diccionario que a cada agente hace corresponder sus commitments.
        Los commitments son una tupla que tiene como primer elemento el porciento de sus ganancias
        que el jugador debe entregar a la recaudacion; mientras que el segundo representa que
        porciento de la recaudacion le corresponde al jugador
        """
        self.id = id
        self.members = set(members)
        self.commitments = commitments
    
    def feed(self, earner_id : int, earnings : int) -> Dict[int, int]:
        """Este metodo, dado el id de un agente y las ganancias que este acaba de obtener,
        reparte de acuerdo a su commitment una porcion de las ganacias entre todos, incluido
        el mismo.\n
        Este metodo retorna un diccionario, de id_agente, ganancia
        """
        distributed_earnings : Dict[int, int] = {}
        taxes = self.commitments[earner_id][0]*earnings
        for member_id in self.members:
            distributed_earnings[member_id] = int(taxes*self.commitments[member_id][1])
        return distributed_earnings
        #En esencia, distribuye la porcion acordada de la ganancia del agente que cobro azucar
        #entre suscompanheros de alianza. La porcion acordada a entregar es el primer componente
        #del commitment de cada agente