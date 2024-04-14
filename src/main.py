import random
from environment.simple_simulation import SimpleSimulation
from environment.map import Map
from environment.agent_handler import Agent_Handler
from environment.simple_range import SimpleWalking, SquareVision
from agents.random_agent import Random_Agent
from random import randint
import pygame

pygame.init()

resources = {}
for i in range(100):
    for j in range(100):
        resources[(i, j)] = (
            random.randint(0, 100) if random.choice([True, False]) else 0
        )
map = Map(100, 100, resources)
positions = set()
while len(positions) < 4:
    new_position = (randint(0, 9), randint(0, 9))
    if not new_position in positions:
        positions.add(new_position)
positions = list(positions)
agents = [
    (
        positions[0],
        (
            1,
            Agent_Handler(
                1, 3, 1, map, Random_Agent(), SimpleWalking(), SquareVision(3)
            ),
        ),
    ),
    (
        positions[1],
        (
            2,
            Agent_Handler(
                2, 5, 1, map, Random_Agent(), SimpleWalking(), SquareVision(3)
            ),
        ),
    ),
    (
        positions[2],
        (
            3,
            Agent_Handler(
                3, 7, 1, map, Random_Agent(), SimpleWalking(), SquareVision(3)
            ),
        ),
    ),
    (
        positions[3],
        (
            4,
            Agent_Handler(
                4, 9, 1, map, Random_Agent(), SimpleWalking(), SquareVision(3)
            ),
        ),
    ),
]

simulation = SimpleSimulation(map, agents)

try:
    while True:
        simulation.step(0.05)  # Actualiza el estado del simulador
except KeyboardInterrupt:
    print("Simulación interrumpida")
finally:
    pygame.quit()
