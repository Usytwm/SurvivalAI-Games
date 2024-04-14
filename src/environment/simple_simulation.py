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
        self.message_area_height = 100  # Altura del área de mensajes
        self.screen_height = self.map.height * self.cell_size + self.message_area_height
        self.screen = pygame.display.set_mode(
            (self.map.width * self.cell_size, self.screen_height)
        )
        self.font = pygame.font.Font(None, 24)
        self.messages = []  # Almacenar los mensajes
        pygame.display.set_caption("Simulation Display")

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

        self.screen.fill((0, 0, 0))  # Fondo negro
        # Define colores para representar los recursos
        # (210, 180, 140)

        terrain_color = (255, 255, 255)  # Un color tipo arena para terreno sin recursos
        resource_color = (139, 69, 19)  # Un color marrón oscuro para recursos al máximo
        agent_color = (255, 0, 0)

        # Dibuja el campo de juego
        for row in range(self.map.height):
            for col in range(self.map.width):
                position = (row, col)
                content = self.map.peek_from_position(position)
                if content:
                    color = agent_color
                elif self.map.resources.get(position, 0) > 0:
                    # Calcula el porcentaje de recursos
                    percentage = self.map.resource_percentage(position)
                    # Interpola los colores en función del porcentaje de recursos
                    color = [
                        int(
                            terrain_color[i]
                            + (resource_color[i] - terrain_color[i]) * percentage
                        )
                        for i in range(3)
                    ]
                else:
                    color = terrain_color  # Sin recursos, usa el color del terreno

                rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Borde negro

                if content:
                    text = self.font.render(str(content), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
                    self.add_message(
                        f"Agente {content} es un tanque."
                    )  # Suponiendo que esto se necesite

        # Mostrar mensajes en el área designada para mensajes
        message_y = (
            self.map.height * self.cell_size + 10
        )  # Comenzar justo debajo del campo de juego
        for message in self.messages:
            message_text = self.font.render(message, True, (255, 255, 255))
            self.screen.blit(message_text, (10, message_y))
            message_y += 30  # Espacio entre mensajes

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
