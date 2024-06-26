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

from copy import deepcopy
from typing import Dict, Tuple, List, Set
from Interfaces.ISimulation import ISimulation, ViewOption
import random
from environment.actions import (
    Action,
    Association_Proposal,
    Attack,
    Association_Creation,
    Action_Type,
)
from environment.graph_of_attacks import Graph_of_Attacks, Component_of_Attacks_Graph
from environment.association import Association
import sys

import pygame
from Interfaces.ISimulation import ISimulation
from environment.agent_handler import Agent_Handler
from environment.map import Map


class Display:
    def __init__(
        self, map: Map, agent_len: int, cell_size=None, max_width=900, max_height=600
    ):
        pygame.init()
        self.map = map
        if cell_size is not None:
            self.cell_size = cell_size
        else:
            max_cell_width = max_width // self.map.width
            max_cell_height = max_height // self.map.height
            self.cell_size = min(max_cell_width, max_cell_height)

        # Calcular las dimensiones de la pantalla basadas en el tamaño de la celda y las dimensiones del mapa
        self.screen_width = self.map.width * self.cell_size
        self.screen_height = self.map.height * self.cell_size
        # self.screen_height = (
        #     self.map.height * self.cell_size + 30 * agent_len
        # )  # 100 pixels for messages area
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.Font(None, 24)
        pygame.display.set_caption("Simulation")

    @staticmethod
    def get_cell_color(position, map: Map, agents, terrain_color, resource_color):
        content = map.peek_from_position(position)

        if content:
            agent = agents.get(content, None)
            return agent.agent.color
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
        self.initial_agents = [agent[1] for agent in agents]
        self.resultPerAgent = []  #! OJO OJO
        self.messages = []  # Almacenar mensajes para la simulación

    @property
    def returnResult(self):  #! OJO OJO, poner para que cuando no halla muerto le de 1
        """
        Returns a tuple (id, results) of the agent in the simulation.
        """
        answer = []
        for id, agent in self.initial_agents:
            try:
                turn_of_death = self.deads[id]
            except:
                turn_of_death = self.turn
            answer.append(
                (
                    id,
                    (
                        turn_of_death / self.turn,
                        self.resourcesPerAgent[id] / self.totalRecursos,
                        (
                            self.AttacksReceivedPerAgent[id] / self.totalAtaques
                            if self.totalAtaques > 0
                            else 0
                        ),
                    ),
                    agent.agent.transition_function,
                )
            )
        return answer

    def add_message(self, message: str):
        self.messages.append(message)

    def __has_ended__(self) -> bool:
        return self.num_of_turns_without_agents_losing_resources > 100 or self.stoped

    def __agents_in_simulation__(self) -> list:
        return self.agents

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
                rnd_id = travellers[random.randint(0, len(travellers) - 1)]
                moves[rnd_id] = destiny
                for id in travellers:
                    if rnd_id != id:
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
                self.add_message(
                    f"Agent {actor_id} attacks Agent {victim_id} with strength {attack_strength}"
                )
                self.agents[actor_id].inform_of_attack_made(
                    victim_id, attack_strength
                )  # el costo de realizar el ataque
                self.agents[victim_id].inform_of_attack_received(
                    actor_id, attack_strength
                )  # el danho que realiza
                action = Attack(actor_id, victim_id, attack_strength)
                self.map.add_action(action)
                if self.agents[victim_id].IsDead:
                    deads.add(victim_id)
                    self.add_message(f"Agent {victim_id} is dead")
                if not victim_id in attackers:
                    attackers[victim_id] = {}
                attackers[victim_id][actor_id] = attack_strength
                self.totalAtaques += 1

        for dead_id in deads:
            action = Action(Action_Type.DIE, dead_id)
            self.map.add_action(action)
            sum_of_strengths = sum(attackers[dead_id].values())
            for attacker_id, attack_strength in attackers[dead_id].items():
                reward = int(
                    (attack_strength * initial_wealth[dead_id]) / sum_of_strengths
                )
                self.__feed_single_agent__(attacker_id, reward, dead_id)
            self.deads[dead_id] = self.turn

    def __execute_association_proposals__(
        self, association_proposals: Dict[int, List[Association_Proposal]]
    ):
        for proposer_id, propositions in association_proposals.items():
            for proposal in propositions:
                accepted = True
                for destinatary_id in proposal.destinataries_ids:
                    accepted = self.agents[
                        destinatary_id
                    ].consider_association_proposal(proposal)
                    if accepted and destinatary_id != proposer_id:
                        self.add_message(
                            f"Agent {destinatary_id} has accepted the proposal from Agent {proposer_id}"
                        )
                if accepted:
                    association = Association(
                        set(proposal.destinataries_ids), proposal.commitments
                    )
                    self.associations[association.id] = association
                    for destinatary_id in proposal.destinataries_ids:
                        self.agents[destinatary_id].inform_joined_association(
                            association
                        )
                        self.map.add_action(
                            Association_Creation(
                                destinatary_id,
                                association.id,
                                association.members,
                                association.commitments,
                            )
                        )

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
                    position, self.map, self.agents, (255, 255, 255), (139, 69, 19)
                )
                self._display.draw_cell(
                    self._display.screen,
                    position,
                    color,
                    self._display.cell_size,
                    self._display.font,
                    self.map,
                )
        # for id, agent in self.agents.items():
        #     self.messages.append(f"Agent {id} has {agent.reserve} sugar")
        self._display.display_messages(self.messages)
        pygame.display.flip()

    def display_terminal(self):
        pass
        # print("____________________")
        # for row in range(0, self.map.height):
        #     line = ""
        #     for column in range(0, self.map.width):
        #         content = self.map.peek_from_position((row, column))
        #         content = content if content else " "
        #         line = line + str(content) + " "
        #     line = line + "|"
        #     print(line)
        # print("____________________")
