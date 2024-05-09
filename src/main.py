import random
import sqlite3
import threading

from httpcore import TimeoutException
from Interfaces.ISimulation import ViewOption
from agents.CombatantAgent.CombatantAgent import CombatantAgent
from agents.ExpertAgent.expert_agent import ExpertAgent
from agents.RandomAgent.random_agent import RandomAgent
from agents.FoodSeekerAgent.FoodSeekerAgent import FoodSeekerAgent
from agents.FoodSeekerAgentwithAstar.FoodSeekerAgentwithAstar import (
    FoodSeekerAgentwithAstar,
)
from agents.PacifistAgent.PacifistAgent import PacifistAgent
from agents.Agent_with_Memories import Agent_with_Memories
from agents.ProAgent.pro_agent import ProAgent
from environment.simple_simulation import SimpleSimulation
from environment.map import Map
from environment.agent_handler import Agent_Handler
from environment.simple_range import SimpleWalking, SquareVision, SquareAttackRange
from random import randint
import pygame
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import google.generativeai as genai
from ai.llm.lm_inference import LLMInterface


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
        reserves = random.randint(1, 100)
        consume = 1
        handler = Agent_Handler(
            agent_id,  # ID único del agente
            reserves,  # Algún valor de configuración
            consume,  # Otro valor de configuración
            map,
            random.choice(
                [
                    FoodSeekerAgentwithAstar(
                        agent_id, consume, reserves, sqlite3.connect(":memory:")
                    ),
                    ProAgent(agent_id, consume, reserves, sqlite3.connect(":memory:")),
                    PacifistAgent(
                        agent_id, consume, reserves, sqlite3.connect(":memory:")
                    ),
                    FoodSeekerAgent(
                        agent_id, consume, reserves, sqlite3.connect(":memory:")
                    ),
                    RandomAgent(
                        agent_id, consume, reserves, sqlite3.connect(":memory:")
                    ),
                    CombatantAgent(
                        agent_id, consume, reserves, sqlite3.connect(":memory:")
                    ),
                    ExpertAgent(
                        agent_id, consume, reserves, sqlite3.connect(":memory:")
                    ),
                ]
            ),  # Objeto del mapa  # Crear una instancia de PacifistAgent con el ID único
            SimpleWalking(),  # Instancia de SimpleWalking
            SquareVision(3),  # Instancia de SquareVision
            SquareAttackRange(3),  # Instancia de SquareAttackRange
        )
        expert_agents.append((position, (agent_id, handler)))
    return expert_agents


def create_simulation(
    width_map,
    height_map,
    num_of_agents,
    view: ViewOption = ViewOption.TERMINAL,
):
    resources = {}
    for i in range(width_map):
        for j in range(height_map):
            if random.choices([True, False]):
                resources[(i, j)] = randint(
                    1, 100
                )  # Pa q no se mueran de hambre y ver sus combates y sus alianzas y eso

    map = Map(width_map, height_map, resources)
    positions = set()
    while len(positions) < num_of_agents:
        new_position = (randint(0, width_map - 1), randint(0, height_map - 1))
        if not new_position in positions:
            positions.add(new_position)
    positions = list(positions)
    agents = create_agents(num_of_agents, positions, map)
    return SimpleSimulation(map, agents, view), [
        (id, type(agent.agent).__name__) for _, (id, agent) in agents
    ]


simulation, details = create_simulation(20, 20, 100, view=ViewOption.PYGAME)
winerr_agents = []


def stop_simulation():
    simulation.stop()


# Configura un temporizador que llamará a stop_simulation después de `timeout` segundos
# timer = threading.Timer(20, stop_simulation)
# timer.start()  # Inicia el temporizador
try:
    while not simulation.__has_ended__():
        winerr_agents = simulation.step(
            sleep_time=0.0001,  # Tiempo de espera entre cada paso
        )  # Actualiza el estado del simulador
except KeyboardInterrupt:
    print("Simulación interrumpida")
finally:
    pygame.quit()