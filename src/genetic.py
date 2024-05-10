import random
import sqlite3
import threading

# from main import create_simulation
from Interfaces.ISimulation import ViewOption
from agents.CombatantAgent.CombatantAgent import CombatantAgent
from agents.ExpertAgent.expert_agent import ExpertAgent
from agents.FoodSeekerAgent.FoodSeekerAgent import FoodSeekerAgent
from agents.PacifistAgent.PacifistAgent import PacifistAgent
from agents.RandomAgent.random_agent import RandomAgent
from environment.agent_handler import Agent_Handler
from environment.map import Map
from environment.simple_range import SimpleWalking, SquareAttackRange, SquareVision
from environment.simple_simulation import SimpleSimulation
from dill import dump, load


def create_agents_genetic(agents, positions, map):
    expert_agents = []
    for i in range(len(agents)):
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
            agents[i],
            SimpleWalking(),  # Instancia de SimpleWalking
            SquareVision(3),  # Instancia de SquareVision
            SquareAttackRange(3),  # Instancia de SquareAttackRange
        )
        expert_agents.append((position, (agent_id, handler)))
    return expert_agents


def create_simulation_genetic(
    width_map,
    height_map,
    agents,
    view: ViewOption = ViewOption.TERMINAL,
):
    resources = {}
    for i in range(width_map):
        for j in range(height_map):
            if random.choices([True, False]):
                resources[(i, j)] = random.randint(
                    1, 100
                )  # Pa q no se mueran de hambre y ver sus combates y sus alianzas y eso

    map = Map(width_map, height_map, resources)
    positions = set()
    while len(positions) < len(agents):
        new_position = (
            random.randint(0, width_map - 1),
            random.randint(0, height_map - 1),
        )
        if not new_position in positions:
            positions.add(new_position)
    positions = list(positions)
    agents = create_agents_genetic(agents, positions, map)
    return SimpleSimulation(map, agents, view), [
        (id, type(agent.agent).__name__) for _, (id, agent) in agents
    ]


A = [((1, [1, 2, 3, 1, 2, 3, 1]), 1), ((2, [3, 2, 1, 1, 1, 3, 1]), 2)]
B = [((1, [1, 1, 1, 1, 1, 3, 1]), 1), ((2, [1, 2, 3, 3, 3, 3, 1]), 2)]


def generar_f(k, q):
    """
    Genera una función de transición f para un autómata finito.

    Args:
        k (int): Número de estados (tipos) en el autómata.
        q (int): Número de símbolos en cada secuencia de transición.

    Returns:
        list: Una lista de tuplas que representa la función de transición f.
              Cada tupla contiene ((estado, adn), estado_destino), donde:
              - estado: El estado actual del autómata.
              - adn: Una secuencia de q símbolos generados aleatoriamente entre 1 y 3.
              - estado_destino: El estado de destino al que transicionar.
    """
    f = []
    for i in range(
        k
    ):  # Por cada estado (Tipo) salen k-1 aristas (Hay una via para ir a los restantes k-1 tipos)
        for j in range(k):
            if j == i:
                continue
            adn = [
                random.randint(1, 3) for _ in range(q)
            ]  # Genera q elementos aleatorios entre 1 y 3
            transitionij = ((i, adn), j)  # Desde i leyendo adn voy hacia j
            f.append(transitionij)  #
    return f


def crear_f_poblacion_inicial(N, K):
    """
    Crea una población inicial de tamaño N, donde cada individuo tiene K estados iniciales posibles.

    Args:
    - N (int): Total de funciones de transicción a devolver.
    - K (int): Número de estados iniciales de cada función de transicción.

    Returns:
    - list: Lista de funciones iniciales.
    """
    fs_iniciales = []
    for _ in range(N):
        f = generar_f(K, 6)  #
        fs_iniciales.append(f)
    return fs_iniciales


def reproducir(padres, tamaño_población):
    """
    Genera una nueva lista de funciones de transicción mediante la reproducción de los padres.

    Args:
    - padres (list): Lista de funciones padres disponibles para la reproducción.
    - tamaño_población (int): Cantidad de funciones a devolver.

    Returns:
    - list: Lista de nuevas funciones (hijas) generadas a partir de los funciones padres.
    """
    hijos = []
    for _ in range(tamaño_población):
        padre1 = random.choice(padres)
        padre2 = random.choice(padres)
        hijo = cruzar_Y_mutar(padre1, padre2)
        hijos.append(hijo)
    return hijos


def mutar(adn):
    """
    Realiza una mutación de un trozo de adn.

    Args:
    - adn (list): array que representa un fragmento de adn.

    Returns:
    - list: array con una posición alterada.
    """
    indice = random.randint(0, len(adn) - 1)

    mutación = random.randint(1, 3)

    adn[indice] = mutación

    return adn


def cruzar_Y_mutar(padre1, padre2):
    """
    Realiza el cruce y la mutación de los fragmentos de adn entre dos funciones padres para generar una función hijo.

    Args:
    - padre1 list[ ((int,list), int) ]: Primer padre para la reproducción.
    - padre2 list[ ((int,list), int) ]: Segundo padre para la reproducción.

    Returns:
    - list[ ((int,list), int) ]: Nuevo individuo (hijo) resultado del cruce y la mutación.
    """
    f_hijo = []
    for k in range(len(padre1)):
        par1 = padre1[k]
        par2 = padre2[k]
        comp1_padre1 = par1[0]
        comp1_padre2 = par2[0]
        adn_K_padre1 = comp1_padre1[1]
        adn_K_padre2 = comp1_padre2[1]
        adn_K_hijo = mezclar_Adn(adn_K_padre1, adn_K_padre2)
        adn_K_hijo = mutar(adn_K_hijo)
        new_estado_adn = (comp1_padre1[0], adn_K_hijo)
        if new_estado_adn not in f_hijo:
            nueva_transiccion = ((comp1_padre1[0], adn_K_hijo), par1[1])
            f_hijo.append(nueva_transiccion)

        else:
            # Realizar alguna acción para manejar la colisión de claves, como ignorarla o modificarla
            adn_k_hijo_extra = mutar(adn_K_hijo)
            nueva_transiccion = ((comp1_padre1[0], adn_k_hijo_extra), par1[1])
            f_hijo.append(nueva_transiccion)
    return f_hijo


def mezclar_Adn(adn_padre1, adn_padre2):
    adn_hijo = [0] * len(adn_padre1)
    punto_de_cruce = random.randint(1, len(adn_padre1) - 2)
    for i in range(0, punto_de_cruce):
        adn_hijo[i] = adn_padre1[i]
    for i in range(punto_de_cruce + 1, len(adn_padre2)):
        adn_hijo[i] = adn_padre2[i]
    return adn_hijo


def función_ponderación(caracterisisticas):
    answer = 0
    for value in caracterisisticas:
        answer += value
    return answer / len(caracterisisticas)


def seleccionar_mejor_poblacións(id_ADN, result, top_k):
    poblacion_ordenada = []
    for i in range(len(result)):
        valor = función_ponderación(result[i][1])

        poblacion_ordenada.append((result[i][0], valor))
    poblacion_ordenada.sort(key=lambda x: x[1], reverse=True)
    mejores_valores = poblacion_ordenada[:top_k]
    mejores_funcionesADN = []
    for id_valor, _ in mejores_valores:
        for id_adn, lista in id_ADN:
            if id_valor == id_adn:
                mejores_funcionesADN.append(lista)
                break  # Salir del bucle interior una vez que se ha encontrado la coincidencia
    return mejores_funcionesADN


def create_agents_ADN(adn_poblacion):
    agents = []
    id = 0

    for adn in adn_poblacion:
        reserve = adn[0][0][1][4]
        reserve = (
            random.randint(150, 1000)
            if reserve == 3
            else random.randint(40, 150) if reserve == 2 else random.randint(1, 40)
        )
        id += 1
        agent = ExpertAgent(id, 1, reserve, sqlite3.connect(":memory:"), adn)
        agents.append(agent)

    return agents, id


def seleccionar_mejor_población(id_ADN, result, top_k):
    poblacion_ordenada = []
    for i in range(0, len(result)):
        valor = función_ponderación(result[i][1])
        poblacion_ordenada.append((result[i], valor))
    poblacion_ordenada.sort(key=lambda x: x[1], reverse=True)
    return poblacion_ordenada[:top_k]


# Función principal
def algoritmo_genético(tamaño_población, generaciones):
    adn_poblacion = crear_f_poblacion_inicial(tamaño_población, 6)
    adn_optimo = []
    for _ in range(generaciones):
        agents, id_ADN = create_agents_ADN(adn_poblacion)

        # TODO Como asocio ADN con agente?
        def stop_simulation():
            simulation.stop()

        # Configura un temporizador que llamará a stop_simulation después de `timeout` segundos
        timer = threading.Timer(20, stop_simulation)
        timer.start()  # Inicia el temporizador
        simulation, agents = create_simulation_genetic(50, 50, agents)
        while not simulation.__has_ended__():
            simulation.step(
                sleep_time=0.0001
            )  # Necesito Turnos que sobrevivio, Recursos que recolecto, combates en los que participo
        timer.cancel()
        result = simulation.returnResult

        # result = {}

        mejor_poblacion = seleccionar_mejor_población(
            id_ADN, result, tamaño_población
        )  # Selecciona los K mejores

        adn_optimo = mejor_poblacion[0][0][
            2
        ]  # Guarda el agente optimo de está generación
        mejor_poblacion = [poblacion[0][2] for poblacion in mejor_poblacion]
        adn_poblacion = reproducir(
            mejor_poblacion, tamaño_población
        )  # Devuelve solo el ADN

    with open("SuperAgente.joblib", "wb") as a:
        dump(adn_optimo, a)


algoritmo_genético(10, 10)


# adn_optimo = None
# with open("SuperAgente.joblib", "rb") as a:
#     adn_optimo = load(a)

# print(adn_optimo)
