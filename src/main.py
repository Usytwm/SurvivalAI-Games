import random
from Interfaces.ISimulation import ViewOption
from agents.PacifistAgent.PacifistAgent import PacifistAgent
#from agents.expert_agent import ExpertAgent
from environment.simple_simulation import SimpleSimulation
from environment.map import Map
from environment.agent_handler import Agent_Handler
from environment.simple_range import SimpleWalking, SquareVision, SquareAttackRange
from agents.random_agent import Random_Agent
from random import randint
import pygame


def create_agents(num_agents, positions, map):
    expert_agents = []
    for i in range(num_agents):
        if i < len(positions):
            position = positions[i]
        else:
            position = positions[
                -1
            ]  # Usar la última posición si no hay suficientes posiciones definidas

        agent_id = i + 1
        handler = Agent_Handler(
            agent_id,  # ID único del agente
            3,  # Algún valor de configuración
            1,  # Otro valor de configuración
            map,  # Objeto del mapa
            PacifistAgent(
                agent_id
            ),  # Crear una instancia de PacifistAgent con el ID único
            SimpleWalking(),  # Instancia de SimpleWalking
            SquareVision(3),  # Instancia de SquareVision
            SquareAttackRange(3),  # Instancia de SquareAttackRange
        )
        expert_agents.append((position, (agent_id, handler)))
    return expert_agents


resources = {}
for i in range(10):
    for j in range(10):
        if random.choices([True, False]):
            resources[(i, j)] = randint(
                1, 100
            )  # Pa q no se mueran de hambre y ver sus combates y sus alianzas y eso
map = Map(10, 10, resources)
positions = set()
while len(positions) < 4:
    new_position = (randint(0, 9), randint(0, 9))
    if not new_position in positions:
        positions.add(new_position)
positions = list(positions)
experts_agents = create_agents(4, positions, map)

simulation = SimpleSimulation(map, experts_agents, view=ViewOption.PYGAME)

try:
    while True:
        simulation.step(sleep_time=0.01)  # Actualiza el estado del simulador
except KeyboardInterrupt:
    print("Simulación interrumpida")
finally:
    pygame.quit()
