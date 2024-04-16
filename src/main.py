import random
from Interfaces.ISimulation import ViewOption
from environment.simple_simulation import SimpleSimulation
from environment.map import Map
from environment.agent_handler import Agent_Handler
from environment.simple_range import SimpleWalking, SquareVision, SquareAttackRange
from agents.random_agent import Random_Agent
from random import randint
import pygame

resources = {}
for i in range(10):
    for j in range(10):
        resources[(i, j)] = (
            1  # Pa q no se mueran de hambre y ver sus combates y sus alianzas y eso
        )
map = Map(10, 10, resources)
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
                1,
                3,
                1,
                map,
                Random_Agent(1),
                SimpleWalking(),
                SquareVision(3),
                SquareAttackRange(3),
            ),
        ),
    ),
    (
        positions[1],
        (
            2,
            Agent_Handler(
                2,
                5,
                1,
                map,
                Random_Agent(2),
                SimpleWalking(),
                SquareVision(3),
                SquareAttackRange(3),
            ),
        ),
    ),
    (
        positions[2],
        (
            3,
            Agent_Handler(
                3,
                7,
                1,
                map,
                Random_Agent(3),
                SimpleWalking(),
                SquareVision(3),
                SquareAttackRange(3),
            ),
        ),
    ),
    (
        positions[3],
        (
            4,
            Agent_Handler(
                4,
                9,
                1,
                map,
                Random_Agent(4),
                SimpleWalking(),
                SquareVision(3),
                SquareAttackRange(3),
            ),
        ),
    ),
]

simulation = SimpleSimulation(map, agents, view=ViewOption.PYGAME)

try:
    while True:
        simulation.step()  # Actualiza el estado del simulador
except KeyboardInterrupt:
    print("Simulación interrumpida")
finally:
    pygame.quit()
