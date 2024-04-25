from typing import Tuple, List, Dict

class Geographic_Memory:
    """Esta clase maneja la memoria del agente relativa a la geografia.\n
    Por ejemplo, mantiene un registro de cuales posiciones existen, de manera que el agente
    puede usarlo para determinar si una posicion se encuentra dentro de los limites de la
    simulacion.\n
    Contiene ademas la informacion relativa a la cantidad de azucar que el agente ha visto
    en cada posicion en cada momento de la simulacion"""
    def __init__(self, id : int):
        self.id = id
        self.valid_positions = set()
        self.actual_sugar_per_position : Dict[Tuple[int, int], int] = {}
        self.last_observation_time : Dict[Tuple[int, int], int] = {}
        self.top_sugar_per_position : Dict[Tuple[int, int], int] = {}
    
    def add_position(self, row : int, column : int):
        """Este metodo anhade una nueva posicion al conjunto de posiciones cuya existencia el
        agente conoce"""
        self.valid_positions.add((row, column))
        self.top_sugar_per_position[(row, column)] = 0
    
    def add_sugar_observation(self, row : int, column : int, iteration : int, resources : int):
        """Dada una posicion y una cantidad de azucar, registra el dato"""
        pos = (row, column)
        self.actual_sugar_per_position[pos] = resources
        self.top_sugar_per_position[pos] = max(self.actual_sugar_per_position[pos], self.top_sugar_per_position[pos])
        self.last_observation_time[pos] = iteration

    def validate_position(self, row : int, column : int) -> bool:
        """Returns True if the agent if the agent knows about the existence of the position
        and otherwise returns False"""
        return (row, column) in self.valid_positions
    
    def get_last_info_of_sugar_in_position(self, row : int, column : int) -> Tuple[int, int]:
        """Dada una posicion returna la cantidad de azucar que habia en ella la ultima vez
        que el agente pudo precisar tal dato.\n
        El valor de retorno es una tupla cuyo primer componente es el numero de la iteracion
        en que se produjo la observacion y cuyo segundo componente es la cantidad de azucar
        que habia en la posicion en tal instante"""
        try:
            return (self.last_observation_time[(row, column)], self.actual_sugar_per_position[(row, column)])
        except:
            return None
    
    def get_top_of_sugar_in_position(self, row : int, column : int) -> int:
        "Dada una posicion retorna la cantidad maxima de azucar que el agente ha visto en ella"
        return self.top_sugar_per_position[(row, column)]