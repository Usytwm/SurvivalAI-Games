import random
from agents.agent import Agent
from environment.arena import MapController


class Simulation:
    def __init__(self, map_width, map_height, num_agents):
        self.map_controller = MapController(map_width, map_height)
        agents = [
            Agent(
                f"{i}",
                10,
                10,
                random.randint(3, 10),
                random.randint(0, map_width - 1),
                random.randint(0, map_height - 1),
                self.map_controller,
            )
            for i in range(num_agents)
        ]
        # Inicializar los agentes en el mapa
        for agent in agents:
            self.map_controller.add_agent(agent)

    def run(self, steps=10):
        for _ in range(steps):
            for agent in self.map_controller.agents:
                if not agent.decide_interaction():
                    # Si no hay interacción, el agente decide moverse
                    dx, dy = agent.decide_next_move()
                    agent.move(dx, dy)
                # dx, dy = agent.next_move()  # El agente decide su próximo movimiento
                # agent.move(dx, dy)  # Intenta ejecutar el movimiento
            self.map_controller.display()


sim = Simulation(10, 10, 3)
sim.run(1000)
