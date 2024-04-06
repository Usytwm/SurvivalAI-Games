from environment.simulation import GameController
from environment.objects import Object_Type, Sim_Object
from agents.random_agent import Random_Agent
#from agents.agent_with_vision import Agent_With_Vision

objects = [
    (0, 0, Sim_Object(1, Object_Type.Agent)),
    (2, 2, Sim_Object(2, Object_Type.Agent)),
    (3, 4, Sim_Object(3, Object_Type.Agent)),
    (1, 1, Sim_Object(4, Object_Type.Agent))
           ]

agents = {
    "1" : Random_Agent(),
    "2" : Random_Agent(),
    "3" : Random_Agent(),
    "4" : Random_Agent()
}

sim = GameController(10, 10, objects, agents)

while(True):
    sim.step()
    input()