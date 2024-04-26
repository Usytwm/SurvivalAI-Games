import random
from Interfaces.ISimulation import ViewOption
from agents.RandomAgent.random_agent import RandomAgent
from agents.FoodSeekerAgent.FoodSeekerAgent import FoodSeekerAgent
from agents.PacifistAgent.PacifistAgent import PacifistAgent

# from agents.expert_agent import ExpertAgent
from environment.simple_simulation import SimpleSimulation
from environment.map import Map
from environment.agent_handler import Agent_Handler
from environment.simple_range import SimpleWalking, SquareVision, SquareAttackRange
from random import randint
import pygame

# import random

# def generate_unique_color(existing_colors):
#     while True:
#         new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#         if new_color not in existing_colors:
#             return new_color

# # Mantén un conjunto de colores existentes para asegurar la unicidad
# existing_colors = set()
# for _ in range(num_agents):
#     agent_color = generate_unique_color(existing_colors)
#     agent = Agent(agent_color)
#     existing_colors.add(agent_color)
#     # agregar el agente a tu sistema de gestión de agentes


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
            map,
            random.choice(
                [
                    PacifistAgent(agent_id),
                    FoodSeekerAgent(agent_id),
                    RandomAgent(agent_id),
                ]
            ),
            # RandomAgent(agent_id),
            # Objeto del mapa  # Crear una instancia del agete con el ID único
            SimpleWalking(),  # Instancia de SimpleWalking
            SquareVision(3),  # Instancia de SquareVision
            SquareAttackRange(3),  # Instancia de SquareAttackRange
        )
        expert_agents.append((position, (agent_id, handler)))
    return expert_agents


resources = {}
for i in range(20):
    for j in range(20):
        # resources[(i, j)] = 1
        if random.choices([True, False]):
            resources[(i, j)] = randint(
                1, 100
            )  # Pa q no se mueran de hambre y ver sus combates y sus alianzas y eso
map = Map(20, 20, resources)
positions = set()
while len(positions) < 5:
    new_position = (randint(0, 19), randint(0, 19))
    if not new_position in positions:
        positions.add(new_position)
positions = list(positions)
experts_agents = create_agents(5, positions, map)

simulation = SimpleSimulation(map, experts_agents, view=ViewOption.PYGAME)

try:
    while True:
        simulation.step(sleep_time=0.02)  # Actualiza el estado del simulador
except KeyboardInterrupt:
    print("Simulación interrumpida")
finally:
    pygame.quit()
