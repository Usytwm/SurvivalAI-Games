from environment.simple_simulation import SimpleSimulation
from environment.map import Map
from environment.agent_handler import Agent_Handler
from environment.simple_range import SimpleWalking
from environment.simple_range import SquareVision
from environment.simple_burrier import Simple_Blurrier
from agents.random_agent import Random_Agent
from random import randint

map = Map(10, 10)
positions = set()
while len(positions) < 4:
    new_position = (randint(0, 9), randint(0, 9))
    if not new_position in positions:
        positions.add(new_position)
positions = list(positions)
agents = [
    (positions[0], (1, Agent_Handler(1, map, Random_Agent(), SimpleWalking(), SquareVision(3), Simple_Blurrier()))),
    (positions[1], (2, Agent_Handler(2, map, Random_Agent(), SimpleWalking(), SquareVision(3), Simple_Blurrier()))),
    (positions[2], (3, Agent_Handler(3, map, Random_Agent(), SimpleWalking(), SquareVision(3), Simple_Blurrier()))),
    (positions[3], (4, Agent_Handler(4, map, Random_Agent(), SimpleWalking(), SquareVision(3), Simple_Blurrier())))
]

simulation = SimpleSimulation(map, agents)

while True:
    simulation.step()