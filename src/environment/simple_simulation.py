"""En esta simulacion simple consideramos lo siguiente, por motivos de simplicidad:
1- Si dos agentes deciden moverse a la misma casilla, ambos se quedan donde estan
2- Los ataques funcionan de la sgte manera:
   - Para realizar un ataque de fuerza k, el atacante debe gastar k azucar
   - Si un agente resulta muerto producto de un ataque, toda su riqueza se distribuye
   entre aquellos que lo atacaron de manera proporcional a la fuerza de sus ataques
   - Una vez que un ataque llega al metodo __execute_attack__, se raliza, no importa si
   durante la ejecucion de tal metodo el agente resulta muerto antes de que el ataque que
   lanzo sea analizado
"""

from typing import Dict, Tuple, List, Set
from Interfaces.ISimulation import ISimulation, ViewOption
from environment.actions import Action, Association_Proposal, Attack, Association_Creation
from environment.graph_of_attacks import Graph_of_Attacks, Component_of_Attacks_Graph
from environment.association import Association
import sys

import pygame
from Interfaces.ISimulation import ISimulation
from environment.agent_handler import Agent_Handler
from environment.map import Map


class Display:
    def __init__(
        self, map: Map, agent_len: int, cell_size=None, max_width=800, max_height=600
    ):
        pygame.init()
        self.map = map
        self.cell_size = (
            cell_size
            if cell_size is not None
            else min(
                max_width // self.map.width,
                (max_height - 30 * agent_len) // self.map.height,
            )
        )
        self.screen_width = self.map.width * self.cell_size
        self.screen_height = (
            self.map.height * self.cell_size + 30 * agent_len
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
        self,
        map: Map,
        agents: List[Tuple[Tuple[int] | Tuple[int | Agent_Handler]]],
        view: ViewOption = ViewOption.TERMINAL,
    ):
        super().__init__(map, agents, view)
        if self.view == ViewOption.PYGAME:
            self._display = Display(map, len(agents))
        self.messages = []  # Almacenar mensajes para la simulación

    def add_message(self, message: str):
        if len(self.messages) > 10:  # Limitar el número de mensajes almacenados
            self.messages.pop(0)
        self.messages.append(message)

    def __get_moves__(self) -> Dict[int, Tuple[int, int]]:
        moves = {}
        destinations: Dict[Tuple[int, int], List[int]] = {}

        for id, agent in self.agents.items():
            current_X, current_Y = self.map.peek_id(id)
            agent.agent.inform_position((current_X, current_Y))
            mov_X, mov_Y = agent.move()
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

    def __execute_attacks__(self, attacks: Dict[int, List[Attack]]):
        initial_wealth = {id: agent.reserve for id, agent in self.agents.items()}
        graph_of_attacks = Graph_of_Attacks(attacks)
        if not graph_of_attacks.empty:
            for attack in graph_of_attacks.connected_components():
                self.__execute_attack__(attack, initial_wealth)

    # Usamos esta modelacion de los ataques como grafos por su expresividad, porque
    # perfectamente nos podra servir para implementar logicas de combate mas complejas, como
    # que si un agente recibe multiples ataques recibe mayor danho al no poder protegerse.
    # Pero para la implementacion simple actual, daria lo mismo usar esta simulacion de grafos
    # como sencillamente una lista con todos los ataques que suceden en el turno
    def __execute_attack__(
        self, graph: Component_of_Attacks_Graph, initial_wealth: Dict[int, int]
    ):
        """Este metodo recibe una de las peleas, descrita como un componente conexo del grafo
        y ademas recibe las riquezas iniciales de los agentes. Ejecuta cada uno de los ataques,
        cobrando a cada agente su costo, infligiendo danhos y repartiendo las riquezas que
        inicialmente tenia un agente entre los agentes que lo atacaron de manera proporcional
        a la fuerza con que lo hicieron
        """
        # attackers almacena para cada agente quien lo ataco y la fuerzo con que lo ataco.
        # Esto es util para luego repartir de manera proprocional la riqueza inicial de la victima
        # entre los atacantes
        attackers: Dict[int, Dict[int, int]] = {}
        deads = set()

        for actor_id, attacks_dict in graph.edges.items():
            for victim_id, attack_strength in attacks_dict.items():
                self.agents[actor_id].inform_of_attack_made(
                    victim_id, attack_strength
                )  # el costo de realizar el ataque
                self.agents[victim_id].inform_of_attack_received(
                    actor_id, attack_strength
                )  # el danho que realiza
                if self.agents[victim_id].IsDead:
                    deads.add(victim_id)
                if not victim_id in attackers:
                    attackers[victim_id] = {}
                attackers[victim_id][actor_id] = attack_strength

        for dead_id in deads:
            sum_of_strengths = sum(attackers[dead_id].values())
            for attacker_id, attack_strength in attackers[dead_id].items():
                reward = int(
                    (attack_strength * initial_wealth[dead_id]) / sum_of_strengths
                )
                self.__feed_single_agent__(attacker_id, reward, dead_id)

    def __execute_association_proposals__(
        self, association_proposals: Dict[int, List[Association_Proposal]]
    ):
        for proposer_id, propositions in association_proposals.items():
            for proposal in propositions:
                accepted = True
                for destinatary_id in proposal.destinataries_ids:
                    accepted = self.agents[destinatary_id].consider_association_proposal(proposal)
                if accepted:
                    association = Association(set(proposal.destinataries_ids), proposal.commitments)
                    self.associations[association.id] = association
                    for destinatary_id in proposal.destinataries_ids:
                        self.agents[destinatary_id].inform_joined_association(association)
                        self.map.add_action(Association_Creation(destinatary_id, association.id, association.members, association.commitments))

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
        for id, agent in self.agents.items():
            self.messages.append(f"Agent {id} has {agent.reserve} sugar")
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