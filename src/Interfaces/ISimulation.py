from enum import Enum
from environment.map import Map
from environment.agent_handler import Agent_Handler
from environment.actions import Action, Action_Type, Attack, Association_Proposal
from environment.association import Association
from typing import List, Dict, Set, Tuple
from random import randint
from abc import ABC, abstractmethod
import time


class ViewOption(Enum):
    TERMINAL = "terminal"
    PYGAME = "pygame"


class ISimulation(ABC):
    def __init__(
        self,
        map: Map,
        agents: List[Tuple[Tuple[int, int], Tuple[int, Agent_Handler]]],
        view: ViewOption,
    ):
        """Recibe los siguientes argumentos:
        - Un mapa ya creado
        - Una diccionario que a cada llave hace corresponder el handler del agente con ese id.
        El handler de cada agente debe tener asociado el mapa global.
        - Una funcion priority que compara dos agentes, para determinar cual va primero
        """
        self.map = map
        self.agents: Dict[int, Agent_Handler] = {}
        self.view = view
        self.objects = (
            {}
        )  # Por ahora los unicos objetos que consideramos en la sim son agentes
        self.associations: Dict[int, Association] = {}
        for position, (id, agent) in agents:
            self.map.insert(position, id)
            self.agents[id] = agent
            self.objects[id] = agent

    def step(
        self,
        sleep_time: float = 0.2,
    ):
        "Move the simulation one step"
        self.__actualize_agents_vision__()
        if self.view == ViewOption.TERMINAL:
            self.display_terminal()
            # input()
        elif self.view == ViewOption.PYGAME:
            self.display()
            time.sleep(sleep_time)
        else:
            raise ValueError("Invalid view option")
        association_proposals = self.__get_association_proposals__()
        attacks = self.__get_attacks__()
        self.__execute_association_proposals__(association_proposals)
        self.__execute_attacks__(attacks)
        moves = self.__get_moves__()
        self.__execute_moves__(moves)
        self.__feed_agents__()
        self.map.grow()

    def __actualize_agents_vision__(self):
        "Passes to all the agents the info about what they can see"
        for agent in self.agents.values():
            print(
                "Agent "
                + str(agent.id)
                + " in position "
                + str(
                    self.map.peek_id(agent.id)
                )  #! obtengo la posicion de un elementio con un id dado
                + " sees:"
            )
            agent.see_objects(self.objects)
            agent.see_resources()
            agent.see_actions()
        self.map.clear_actions()

    @abstractmethod
    def __get_moves__(self) -> Dict[int, Tuple[int, int]]:
        """Get the moves from all players. Returns a dictionary corresponding a destiny for each
        moving agent"""
        pass

    def __execute_moves__(self, moves: Dict[int, Tuple[int, int]]):
        "Move each agent to its destination"
        for id, destiny in moves.items():
            self.map.move(id, destiny)
            self.agents[id].inform_move(destiny)

    def __get_association_proposals__(self) -> Dict[int, List[Association_Proposal]]:
        """Devuelve un diccionario donde a cada id de agente le hace corresponder la lista de
        acciones relacionadas con Asociaciones que realizara en este turno."""
        association_proposals = {}
        for id, agent in self.agents.items():
            association_proposals[id] = agent.get_association_proposals()
        return association_proposals

    def __get_attacks__(self) -> Dict[int, List[Attack]]:
        """Devuelve un diccionario donde a cada id de agente le hace corresponder la lista de
        los ataques que el agente desea realizar en este turno"""
        attacks = {}
        for id, agent in self.agents.items():
            attacks[id] = agent.get_attacks()
        return attacks

    def __validate_action__(self, action: Action) -> bool:
        # Por Ahora
        return True

    @abstractmethod
    def __execute_association_proposals__(
        self, association_proposals: Dict[int, List[Association_Proposal]]
    ):
        """Ejecuta las acciones relacionadas con Asociaciones de este turno, y coloca en el
        mapa de las acciones ocurridas en el ultimo turno a aquellas que lo requieran"""
        pass

    @abstractmethod
    def __execute_attacks__(self, actions: Dict[int, List[Attack]]):
        """Ejecuta los ataques provistos, y los hace visibles colocandolos en el mapa de
        acciones del ultimo turno"""
        pass

    def __feed_agents__(self):
        """Feed each agent with the amount of sugar that there is in its cell and substracts
        his consume from his reserve"""
        for agent_id, agent in self.agents.items():
            crop = self.map.feed(agent_id)
            self.__feed_single_agent__(agent_id, crop)
            agent.burn()

        for agent in list(self.agents.values()):
            if agent.IsDead:
                self.map.add_action(Action(Action_Type.DIE, agent.id))
                self.__remove_agent__(agent.id)

    def __feed_single_agent__(self, id: int, sugar: int, victim_id=None):
        agent = self.agents[id]
        if agent.IsAssociated:
            for association_id in agent.associations:
                distribution = self.associations[association_id].feed(id, sugar)
                for ally_id, portion in distribution.items():
                    if victim_id:
                        self.agents[ally_id].take_attack_reward(victim_id, portion)
                    else:
                        self.agents[ally_id].feed(portion)
        taxes_excented = int(agent.free_portion * sugar)
        if victim_id:
            agent.take_attack_reward(victim_id, taxes_excented)
        else:
            agent.feed(taxes_excented)

    def __remove_agent__(self, id: int):
        self.agents.pop(id)
        self.objects.pop(id)
        self.map.pop_id(id)

    @abstractmethod
    def display(self):
        "Shows whats happening"
        pass

    @abstractmethod
    def display_terminal(self):
        pass
