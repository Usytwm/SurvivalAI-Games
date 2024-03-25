class Map:
    """
    Representa el mapa de la simulación, incluyendo el terreno y los objetos colocados en él.

    Atributos:
        width (int): Ancho del mapa.
        height (int): Alto del mapa.
        terrain (list): Matriz que representa el terreno del mapa.
        objects (dict): Diccionario de objetos colocados en el mapa, indexados por su posición (x, y).
    """

    def __init__(self, width, height):
        """
        Inicializa una nueva instancia del mapa con las dimensiones especificadas.

        Parámetros:
            width (int): Ancho del mapa.
            height (int): Alto del mapa.
        """
        self.width = width
        self.height = height
        self.terrain = [[None for _ in range(width)] for _ in range(height)]
        # self.objects = {}  # {(x, y): object}

    def update_cell(self, x, y, content):
        if not self.valid_position(x, y):
            raise ValueError("Invalid position for object")
        self.terrain[y][x] = content

    def cell_content(self, x, y):
        if not self.valid_position(x, y):
            raise ValueError("Invalid position")
        return self.terrain[y][x]

    def valid_position(self, x, y):
        """
        Verifica si una posición dada está dentro de los límites del mapa.

        Parámetros:
            x (int): La posición x a verificar.
            y (int): La posición y a verificar.

        Retorna:
            bool: True si la posición es válida, False en caso contrario.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    # def display1(self):
    #     # Method to print the map on console (optional for debugging)
    #     for row in self.terrain:
    #         print(" ".join(str(cell) if cell else "_" for cell in row))

    def display(self):
        max_width = 0
        for row in self.terrain:
            for cell in row:
                cell_length = len(str(cell) if cell else "-")
                max_width = max(max_width, cell_length)

        top_bottom_border = "-" + "-" * (
            max_width * len(self.terrain[0]) + len(self.terrain[0])
        )

        print(top_bottom_border)  # Imprime el borde superior.
        for row in self.terrain:
            # Creamos la fila con cada celda ajustada al ancho máximo.
            row_str = "|"
            for cell in row:
                row_str += (
                    str(cell).ljust(max_width) + " "
                )  # Aseguramos que cada celda tenga el mismo ancho.
            print(
                row_str[:-1] + "|"
            )  # Imprimimos la fila y eliminamos el último espacio antes del borde derecho.
        print(top_bottom_border)  # Imprime el borde inferior.


class Agent:
    """
    Representa un agente en la simulación, capaz de moverse, recoger objetos e interactuar con otros agentes.

    Atributos:
        name (str): Nombre del agente.
        health (int): Salud actual del agente.
        x (int): Posición x actual del agente en el mapa.
        y (int): Posición y actual del agente en el mapa.

    """

    def __init__(self, name, health, x, y):
        """
        Inicializa una nueva instancia de un agente.

        Parámetros:
            name (str): Nombre del agente.
            health (int): Salud inicial del agente.
            x (int): Posición x inicial del agente.
            y (int): Posición y inicial del agente.
        """
        self.name = name
        self.health = health
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """
        Mueve el agente en el mapa según los desplazamientos especificados.

        Parámetros:
            dx (int): Desplazamiento en el eje x.
            dy (int): Desplazamiento en el eje y.
        """
        self.x += dx
        self.y += dy

    def interact(self, other_agent):
        """
        Define la lógica de interacción entre este agente y otro. Esto podría incluir combatir, formar alianzas, intercambiar objetos, etc.

        Parámetros:
            other_agent (Agent): El otro agente con el cual este agente interactúa.
        """
        # Interaction logic (fighting, forming alliances, etc.)
        pass

    def __str__(self) -> str:
        return self.name


class Human_Agent(Agent):
    """
    Clase que representa un agente humano en la simulación, capaz de tomar decisiones basadas en su entorno y estado.

    Atributos:
        name (str): Nombre del agente.
        health (int): Salud actual del agente.
        x (int): Posición x actual del agente en el mapa.
        y (int): Posición y actual del agente en el mapa.
        inventory (list): Inventario de objetos que el agente ha recogido.
        state (dict): Diccionario para almacenar estados adicionales del agente (hambre, sed, etc.).
    """

    def __init__(self, name, health, x, y):
        """
        Inicializa una nueva instancia de un agente humano.

        Parámetros:
            name (str): Nombre del agente.
            health (int): Salud inicial del agente.
            x (int): Posición x inicial del agente.
            y (int): Posición y inicial del agente.
            inventario (list): Lista de objetos que el agente ha recogido.
            state (dict): Diccionario para almacenar estados adicionales del agente (hambre, sed, etc.).
        """
        super().__init__(name, health, x, y)
        self.inventory = []
        self.state = {}

    def decide_actions(self):
        """
        Implementar la lógica para que el agente humano tome decisiones basadas en su entorno y estado actual.
        """
        # Decision-making logic
        pass

    def pick_up_object(self, obj):
        """
        Añade un objeto al inventario del agente.

        Parámetros:
            obj (Object): El objeto a recoger.
        """
        self.inventory.append(obj)


import time


class Simulation:
    def __init__(self, map_width, map_height, num_agents):
        self.map = Map(map_width, map_height)
        self.agents = [Agent(f"Agent {i}", 100, i, i) for i in range(num_agents)]
        for agent in self.agents:
            self.map.update_cell(agent.x, agent.y, agent)

    def execute_cycle(self):
        for agent in self.agents:
            agent.move(1, 0)  # Move to the right

    def start(self):
        while True:
            self.execute_cycle()
            self.map.display()
            time.sleep(1)


sim = Simulation(10, 10, 4)
sim.start()


class Object:
    """
    Clase base para objetos que pueden ser colocados en el mapa.

    Atributos:
        name (str): Nombre del objeto.
    """

    def __init__(self, name):
        """
        Inicializa una nueva instancia de un objeto.

        Parámetros:
            name (str): El nombre del objeto.
        """
        self.name = name


class Food(Object):
    """
    Representa un objeto de comida que puede ser consumido por los agentes.

    Atributos:
        nutritional_amount (int): La cantidad de nutrición que proporciona la comida.
    """

    def __init__(self, nutritional_amount):
        """
        Inicializa una nueva instancia de comida.

        Parámetros:
            nutritional_amount (int): La cantidad de nutrición que proporciona la comida.
        """
        super().__init__("Food")
        self.nutritional_amount = nutritional_amount


class Weapon(Object):
    """
    Representa un arma que puede ser utilizada por los agentes para luchar.

    Atributos:
        damage (int): El daño que el arma puede infligir.
    """

    def __init__(self, damage):
        """
        Inicializa una nueva instancia de un arma.

        Parámetros:
            damage (int): El daño que el arma puede infligir.
        """
        super().__init__("Weapon")
        self.damage = damage
