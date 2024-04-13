"""En esta simulacion simple consideramos lo siguiente, por motivos de simplicidad:
1- Si dos agentes deciden moverse a la misma casilla, ambos se quedan donde estan
"""
from typing import Dict, Tuple, List
from Interfaces.ISimulation import ISimulation
class SimpleSimulation(ISimulation):
    def __get_moves__(self) -> Dict[int, Tuple[int, int]]:
        moves = {}
        destinations : Dict[Tuple[int, int], List[int]] = {}
        
        for id, agent in self.agents.items():
            destiny = agent.move()
            if not destiny in destinations:
                destinations[destiny] = []
            destinations[destiny].append(id)
        
        for destiny, travellers in destinations.items():
            if len(travellers) > 1:
                for id in travellers:
                    moves[id] = self.map.peek_id(id) #o sea, no se mueve
            else:
                moves[travellers[0]] = destiny
        
        return moves
    
    def display(self):
        print("____________________")
        for row in range(0, self.map.height):
            line = ""
            for column in range(0, self.map.width):
                content = self.map.peek_from_position((row, column))
                content = content if content else " "
                line = line + str(content) + " "
            line = line + '|'
            print(line)
        print("____________________")