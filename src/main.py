from environment.simulation import GameController
from environment.objects import Object_Type, Sim_Object
from agents.just_moves_randomly_agent import Just_Moves_Randomly_Agent

objects = [
    (0, 0, Sim_Object(1, Object_Type.Agent)),
    (2, 2, Sim_Object(2, Object_Type.Agent)),
    (3, 4, Sim_Object(3, Object_Type.Agent)),
    (6, 6, Sim_Object(4, Object_Type.Agent))
           ]

agents = {
    "1" : Just_Moves_Randomly_Agent(),
    "2" : Just_Moves_Randomly_Agent(),
    "3" : Just_Moves_Randomly_Agent(),
    "4" : Just_Moves_Randomly_Agent()
}

sim = GameController(10, 10, objects, agents)

while(True):
    sim.step()
    input()