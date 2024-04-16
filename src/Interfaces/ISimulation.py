from enum import Enum
from environment.map import Map
from environment.agent_handler import Agent_Handler
from environment.actions import Action, Action_Type
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
            self.agents.copy()
        )  # Por ahora los unicos objetos que consideramos en la sim son agentes
        self.associations : Dict[int, Association] = {}
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
            input()
        elif self.view == ViewOption.PYGAME:
            self.display()
            time.sleep(sleep_time)
        else:
            raise ValueError("Invalid view option")
        actions = self.__get_actions__()
        for id, action_list in actions.items():
            for action in action_list:
                self.map.add_action(action)
        self.__execute_actions__(actions)
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
                + str(self.map.peek_id(agent.id))
                + "sees:"
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

    def __get_actions__(self) -> Dict[int, List[Action]]:
        """Devuelve un diccionario donde a cada id de agente le hace corresponder la lista de
        acciones que desea tomar en este turno tal agente"""
        actions = {}
        for id, agent in self.agents.items():
            actions[id] = [
                act for act in agent.get_actions() if self.__validate_action__(act)
            ]
        return actions

    def __validate_action__(self, action: Action) -> bool:
        # Por Ahora
        return True

    @abstractmethod
    def __execute_actions__(self, actions: Dict[int, List[Action]]):
        """Ejecuta las acciones provistas en actions"""
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

    def __feed_single_agent__(self, id : int, sugar : int, victim_id = None):
        agent = self.agents[id]
        if agent.IsAssociated:
            for association_id in agent.associations:
                distribution = self.associations[association_id].feed(id, sugar)
                for ally_id, portion in distribution.items():
                    if victim_id:
                        self.agents[ally_id].take_attack_reward(victim_id, portion)
                    else:
                        self.agents[ally_id].feed(portion)
        taxes_excented = int(agent.free_portion*sugar)
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
