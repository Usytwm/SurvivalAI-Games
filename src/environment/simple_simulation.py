"""En esta simulacion simple consideramos lo siguiente, por motivos de simplicidad:
1- Si dos agentes deciden moverse a la misma casilla, ambos se quedan donde estan
"""

import sys
from typing import Dict, Tuple, List

import pygame
from Interfaces.ISimulation import ISimulation
from environment.agent_handler import Agent_Handler
from environment.map import Map


class SimpleSimulation(ISimulation):

    def __init__(
        self, map: Map, agents: List[Tuple[Tuple[int] | Tuple[int | Agent_Handler]]]
    ):
        super().__init__(map, agents)
        self.cell_size = 50
        self.screen = pygame.display.set_mode(
            (self.map.width * self.cell_size, self.map.height * self.cell_size)
        )
        pygame.display.set_caption("Simulation Display")

    def __get_moves__(self) -> Dict[int, Tuple[int, int]]:
        moves = {}
        destinations: Dict[Tuple[int, int], List[int]] = {}

        for id, agent in self.agents.items():
            mov_X, mov_Y = agent.move()
            current_X, current_Y = self.map.peek_id(id)
            destiny = (mov_X + current_X, mov_Y + current_Y)
            if not destiny in destinations:
                destinations[destiny] = []
            destinations[destiny].append(id)

        for destiny, travellers in destinations.items():
            if len(travellers) > 1:
                for id in travellers:
                    moves[id] = self.map.peek_id(id)  # o sea, no se mueve
            else:
                moves[travellers[0]] = destiny

        return moves

    def display1(self):
        print("____________________")
        for row in range(0, self.map.height):
            line = ""
            for column in range(0, self.map.width):
                content = self.map.peek_from_position((row, column))
                content = content if content else " "
                line = line + str(content) + " "
            line = line + "|"
            print(line)
        print("____________________")

    def display(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill((0, 0, 0))  # Fondo negro
        for row in range(self.map.height):
            for col in range(self.map.width):
                content = self.map.peek_from_position((row, col))
                color = (
                    (255, 0, 0) if content else (255, 255, 255)
                )  # Rojo si hay un agente, blanco si está vacío
                rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)  # Borde negro

        pygame.display.flip()
