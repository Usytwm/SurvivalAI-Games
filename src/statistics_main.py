import threading
from httpcore import TimeoutException
from Interfaces.ISimulation import ViewOption
import pygame
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from main import create_simulation

import os

# Define la ruta del directorio donde se guardarán las imágenes
OUTPUT_DIR = "D:/Escuela/Projects/IA y Simulacion/SurvivalAI-Games/data"

# Asegúrate de que el directorio existe, si no, créalo
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def save_plot(filename):
    # Construye la ruta completa donde se guardará la imagen
    full_path = os.path.join(OUTPUT_DIR, f"{filename}.png")
    plt.savefig(full_path)


random_victories = {}
food_Seeker_victories = {}
combat_agent_victories = {}
pacifist_agent_victories = {}


def run_multiple_simulations(
    num_simulations, map_width, map_height, num_agents, timeout=20
):
    results = []

    for i in range(num_simulations):
        random_victories[i] = 0
        food_Seeker_victories[i] = 0
        combat_agent_victories[i] = 0
        pacifist_agent_victories[i] = 0
        simulation = create_simulation(
            map_width, map_height, num_agents, view=ViewOption.TERMINAL
        )
        winner_agents = []

        def stop_simulation():
            simulation.stop()

        # Configura un temporizador que llamará a stop_simulation después de `timeout` segundos
        timer = threading.Timer(timeout, stop_simulation)
        timer.start()  # Inicia el temporizador
        try:
            while not simulation.__has_ended__():
                winner_agents = simulation.step(sleep_time=0.0001)
        except KeyboardInterrupt:
            timer.cancel()
            continue
        finally:
            pygame.quit()
            timer.cancel()

        for agent_id, handler in winner_agents.items():
            results.append(
                {
                    "AgentID": agent_id,
                    "AgentType": type(handler.agent).__name__,
                    "InitialReserves": handler.initial_reserve,
                    "AssociationsCount": handler.associations_count,
                    "FinalReserves": handler.reserve,
                    "Victories": 1,
                }
            )
            if type(handler.agent).__name__ == "RandomAgent":
                random_victories[i] += 1
            elif type(handler.agent).__name__ == "FoodSeekerAgent":
                food_Seeker_victories[i] += 1
            elif type(handler.agent).__name__ == "CombatantAgent":
                combat_agent_victories[i] += 1
            elif type(handler.agent).__name__ == "PacifistAgent":
                pacifist_agent_victories[i] += 1
        print(f"Step {i + 1} of {num_simulations} completed")
    return pd.DataFrame(results)


def plot_and_save(num_simulations, map_width, map_height, num_agents):
    # * OK
    def analyze_agent_wins(df):
        win_counts = df["AgentType"].value_counts()
        plt.figure(figsize=(10, 6))
        sns.barplot(x=win_counts.index, y=win_counts.values)
        plt.title("Frecuencia de Victorias por Tipo de Agente")
        plt.xlabel("Tipo de Agente")
        plt.ylabel("Número de Victorias")
        filename = f"agent_wins_num_simulations{num_simulations}_size({map_width}x{map_height})_agents_count{num_agents}"
        save_plot(filename)
        plt.show()
        return win_counts

    # Función para analizar la correlación entre victorias y asociaciones
    def analyze_associations_correlation(df):
        # Agrupar por tipo de agente para consolidar datos por tipo
        grouped_df = (
            df.groupby("AgentType")
            .agg(
                {
                    "Victories": "sum",  # Sumar el número de victorias por tipo de agente
                    "AssociationsCount": "mean",  # Promedio de asociaciones por tipo de agente
                }
            )
            .reset_index()
        )

        # Visualizar la correlación con un gráfico de dispersión usando colores únicos para cada tipo de agente
        plt.figure(figsize=(10, 6))
        # Generar una paleta de colores única para cada tipo de agente
        palette = sns.color_palette("hsv", len(grouped_df["AgentType"].unique()))
        sns.scatterplot(
            data=grouped_df,
            x="Victories",
            y="AssociationsCount",
            hue="AgentType",
            palette=palette,
            s=100,
        )

        plt.title(
            "Correlación entre Número de Asociaciones y Victorias por Tipo de Agente"
        )
        plt.xlabel("Total de Victorias")
        plt.ylabel("Promedio de Asociaciones")
        plt.legend(title="Tipo de Agente")
        plt.grid(True)  # Añadir una cuadrícula para mejor visualización
        filename = f"associations_correlation_num_simulations{num_simulations}_size({map_width}x{map_height})_agents_count{num_agents}"
        plt.show()

        # Calcular y mostrar el valor de la correlación
        correlation = grouped_df["Victories"].corr(grouped_df["AssociationsCount"])
        print(f"Correlación por Tipo de Agente: {correlation}")

    # * OK
    def plot_victories_by_type_and_simulation(
        random_victories,
        food_Seeker_victories,
        combat_agent_victories,
        pacifist_agent_victories,
    ):
        # Crear un DataFrame a partir de los diccionarios
        df = pd.DataFrame(
            {
                "RandomAgent": random_victories,
                "FoodSeekerAgent": food_Seeker_victories,
                "CombatantAgent": combat_agent_victories,
                "PacifistAgent": pacifist_agent_victories,
            }
        )

        # Graficar los resultados como funciones con diferentes colores
        plt.figure(figsize=(12, 6))
        plt.plot(
            df.index,
            df["RandomAgent"],
            label="RandomAgent",
            linestyle="-",
            color="red",
        )
        plt.plot(
            df.index,
            df["FoodSeekerAgent"],
            label="FoodSeekerAgent",
            linestyle="-",
            color="green",
        )
        plt.plot(
            df.index,
            df["CombatantAgent"],
            label="CombatantAgent",
            linestyle="-",
            color="blue",
        )
        plt.plot(
            df.index,
            df["PacifistAgent"],
            label="PacifistAgent",
            linestyle="-",
            color="purple",
        )

        plt.title("Victorias por Tipo de Agente en Cada Simulación")
        plt.xlabel("Número de Simulación")
        plt.ylabel("Cantidad de Victorias")
        plt.legend(title="Tipo de Agente")
        plt.grid(True)  # Añadir una cuadrícula para mejor visualización
        filename = f"victories_by_type_num_simulations{num_simulations}_size({map_width}x{map_height})_agents_count{num_agents}"
        save_plot(filename)
        plt.show()

    # *Ok Función para analizar el cambio en las reservas
    def analyze_reserves_change(df):
        # Asegurar que la columna 'ReserveChange' está en el DataFrame
        if "ReserveChange" not in df.columns:
            df["ReserveChange"] = df["FinalReserves"] - df["InitialReserves"]

        # Preparar el DataFrame para el gráfico
        df_sorted = df.sort_values(by="AgentType")

        # Visualizar el cambio en las reservas con un gráfico de dispersión
        plt.figure(figsize=(10, 6))
        sns.stripplot(
            data=df_sorted,
            x="AgentType",
            y="ReserveChange",
            jitter=True,
            size=5,
            alpha=0.6,
        )
        plt.title("Cambio en las Reservas por Tipo de Agente")
        plt.xlabel("Tipo de Agente")
        plt.ylabel("Cambio en las Reservas")
        plt.xticks(rotation=0)  # Rotar las etiquetas para mejor visualización
        plt.grid(True)  # Añadir una cuadrícula
        filename = f"reserves_change_num_simulations{num_simulations}_size({map_width}x{map_height})_agents_count{num_agents}"
        save_plot(filename)
        plt.show()

    # * OK
    def calculate_association_metrics(results_df):
        # Crear una nueva columna que indica si el agente tenía asociaciones o no
        results_df["HasAssociations"] = results_df["AssociationsCount"] > 0

        # Calcular la cantidad de ganadores con y sin asociaciones
        association_stats = (
            results_df["HasAssociations"].value_counts(normalize=True) * 100
        )

        # Visualizar los resultados
        fig, ax = plt.subplots()
        association_stats.plot(kind="bar", color=["blue", "red"], ax=ax)
        ax.set_title("Porcentaje de Ganadores con y sin Asociaciones")
        ax.set_xlabel("Tiene Asociaciones")
        ax.set_ylabel("Porcentaje (%)")
        # Asegurarse de que las etiquetas reflejen correctamente los datos
        ax.set_xticklabels(["Sin Asociaciones", "Con Asociaciones"], rotation=0)
        filename = f"association_metrics_num_simulations{num_simulations}_size({map_width}x{map_height})_agents_count{num_agents}"
        save_plot(filename)
        plt.show()

        # Imprimir los resultados
        print(association_stats)

    results_df = run_multiple_simulations(
        num_simulations, map_width, map_height, num_agents
    )
    # Ejecución de análisis
    win_counts = analyze_agent_wins(results_df)
    analyze_associations_correlation(results_df)
    plot_victories_by_type_and_simulation(
        random_victories,
        food_Seeker_victories,
        combat_agent_victories,
        pacifist_agent_victories,
    )
    analyze_reserves_change(results_df)
    calculate_association_metrics(results_df)


plot_and_save(10000, 20, 20, 100)
