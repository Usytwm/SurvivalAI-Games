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
        self.add_position(row, column)
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
    
    def get_position_with_most_sugar(self, row : int, column : int) -> Tuple[Tuple[int, int], int]:
        """Dada la posicion en que se encuentra el agente actualmente, devuelve la posicion
        de mas azucar que el agente ha visto y la cantidad de azucar que tenia en el momento
        de la observacion"""
        answer = None
        for position, resources in self.actual_sugar_per_position.items():
            if position == (row, column):
                continue
            if not answer:
                answer = (position, resources)
                continue
            if answer[1] < resources:
                answer = (position, resources)
        return answer
    
    def get_max_sugar_around_position(self, row : int, column : int):
        """Dada una posicion, retorna cual la mayor cantidad de azucar entre las nueve casillas
        a su alrededor"""
        max_sugar_around = 0
        for r in range(row - 1, row + 1):
            for c in range(column - 1, column + 1):
                if r == row and c == column:
                    continue
                try:
                    max_sugar_around = max(max_sugar_around, self.get_last_info_of_sugar_in_position(r, c)[1])
                except:
                    pass
        return max_sugar_around