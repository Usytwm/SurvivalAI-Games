"""En esta simulacion simple consideramos lo siguiente, por motivos de simplicidad:
1- Si dos agentes deciden moverse a la misma casilla, ambos se quedan donde estan
"""

import sys
from typing import Dict, Tuple, List

import pygame
from Interfaces.ISimulation import ISimulation
from environment.agent_handler import Agent_Handler
from environment.map import Map


class Display:
    def __init__(self, map: Map, cell_size=None, max_width=800, max_height=600):
        self.map = map
        self.cell_size = (
            cell_size
            if cell_size is not None
            else min(max_width // self.map.width, (max_height - 100) // self.map.height)
        )
        self.screen_width = self.map.width * self.cell_size
        self.screen_height = (
            self.map.height * self.cell_size + 100
        )  # 100 pixels for messages area
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.Font(None, 24)
        pygame.display.set_caption("Simulation")

    @staticmethod
    def get_cell_color(position, map: Map, agent_color, terrain_color, resource_color):
        content = map.peek_from_position(position)
        if content:
            return agent_color
        elif map.resources.get(position, 0) > 0:
            percentage = map.resource_percentage(position)
            return [
                int(
                    terrain_color[i]
                    + (resource_color[i] - terrain_color[i]) * percentage
                )
                for i in range(3)
            ]
        else:
            return terrain_color

    @staticmethod
    def draw_cell(screen, position, color, cell_size, font, map: Map, border=0):
        rect = pygame.Rect(
            position[1] * cell_size, position[0] * cell_size, cell_size, cell_size
        )
        pygame.draw.rect(screen, color, rect)
        if border > 0:
            pygame.draw.rect(screen, (0, 0, 0), rect, border)
        content = map.peek_from_position(position)
        if content:
            text = font.render(str(content), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    def display_messages(self, messages):
        message_y = self.map.height * self.cell_size + 10
        for message in messages:
            message_text = self.font.render(message, True, (255, 255, 255))
            self.screen.blit(message_text, (10, message_y))
            message_y += 30


class SimpleSimulation(ISimulation):

    def __init__(
        self, map: Map, agents: List[Tuple[Tuple[int] | Tuple[int | Agent_Handler]]]
    ):
        super().__init__(map, agents)
        self._display = Display(
            map,
        )
        self.messages = []  # Almacenar mensajes para la simulación

    def add_message(self, message: str):
        if len(self.messages) > 10:  # Limitar el número de mensajes almacenados
            self.messages.pop(0)
        self.messages.append(message)

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

    def display(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self._display.screen.fill((0, 0, 0))  # Limpiar pantalla para nuevo frame

        # Dibujar y mostrar mensajes
        for row in range(self.map.height):
            for col in range(self.map.width):
                position = (row, col)
                color = self._display.get_cell_color(
                    position, self.map, (255, 0, 0), (255, 255, 255), (139, 69, 19)
                )
                self._display.draw_cell(
                    self._display.screen,
                    position,
                    color,
                    self._display.cell_size,
                    self._display.font,
                    self.map,
                )

        self._display.display_messages(self.messages)
        pygame.display.flip()
        self.messages = []  # Limpia los mensajes después de mostrarlos

    def display_terminal(self):
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
