import sqlite3
from typing import Tuple, List, Dict

CREATE_TABLE = """CREATE TABLE %s (agent_id INTEGER, row INTEGER, column INTEGER,
iteration INTEGER, resources INTEGER)"""
INSERT_APPEARENCE = """INSERT INTO %s (agent_id, row, column, iteration, resources) VALUES(%s, %s, %s, %s, %s);"""
SELECT_QUERY = """SELECT * FROM %s"""
QUERY_FOR_LAST_APPEARENCE_OF_AGENT = (
    """SELECT * FROM %s WHERE agent_id = %s ORDER BY iteration DESC LIMIT 1"""
)
QUERY_FOR_ALL_APPEARENCES_OF_AGENT = (
    """SELECT * FROM %s WHERE agent_id = %s ORDER BY iteration DESC"""
)
QUERY_FOR_LAST_APPEARENCE_IN_A_POSITION = """SELECT * FROM %s WHERE row = %s AND column = %s ORDER BY iteration DESC LIMIT 1"""
QUERY_FOR_ALL_APPEARENCES_IN_A_POSITION = (
    """SELECT * FROM %s WHERE row = %s AND column = %s ORDER BY iteration DESC"""
)


class Memory_for_Agents_Sights:
    """Una instancia de esta clase corresponde a la memoria que tiene un agente acerca de
    donde, cuando y como ha observado a otros agentes\n
    Esta clase funciona accediendo a una tabla de sqlite guardada en memoria (no es persistente)\n
    Cada fila de la tabla describe la observacion de otro agente por parte del agente cuya
    memoria estamos controlando. Tal observacion es descrita usando el id del agente observado
    la posicion en que fue observado, la fecha en que fue observado, la cantidad de azucar que
    traia consigo asi como otros detalles que se puedan ir incluyendo.
    """

    def __init__(self, id, conn: sqlite3.Connection):
        """Para instanciar esta clase necesitamos el id del agente cuya memoria sera controlada
        por la instancia.\n En este metodo ademas creamos la tabla asociada a este agente
        y por ello en el momento de instanciar necesitamos la conexion donde se creara esa tabla
        """
        self.id = id
        self.cursor = conn.cursor()
        self.table_name = "agents_sights_" + str(self.id)
        self.cursor = self.cursor.execute(CREATE_TABLE % (self.table_name))
        self.agents_seen = {} #para cada agente guarda cuantas veces ha sido vistp

    def add_appearence(
        self, other_id: int, row: int, column: int, iteration: int, resources: int
    ):
        """Anhade a la base de datos la observacion de una posicion.\n
        La observacion es descrita con el id del agente observado, la iteracion en que ocurrio
        la observacion y la cantidad de azucar que llevaba el agente observado.\n"""
        self.cursor = self.cursor.execute(
            INSERT_APPEARENCE
            % (self.table_name, other_id, row, column, iteration, resources)
        )
        if other_id is not None:
            self.agents_seen[other_id] = self.agents_seen.get(other_id, 0) + 1

    def add_empty_sight(self, position: Tuple[int, int], iteration: int):
        """Anhade a la base de datos la observacion de que una posicion se encuentra vacia"""
        self.cursor = self.cursor.execute(
            INSERT_APPEARENCE
            % (self.table_name, "NULL", position[0], position[1], iteration, "NULL")
        )

    def get_last_info_from_agent(self, other_id) -> Tuple[Tuple[int, int], int, int]:
        """Devuelve la ultima informacion recolectada sobre el agente cuyo id fue provisto.\n
        El valor de devuelto es una tupla que contiene la posicion donde estaba como primer
        componente, el momento en que fue visto como segunda componente
        y la cantidad de azucar que llevaba como tercero\n
        Returna None si no ha visto al agente"""
        last_observation = self.cursor.execute(
            QUERY_FOR_LAST_APPEARENCE_OF_AGENT % (self.table_name, str(other_id))
        ).fetchall()
        if len(last_observation) == 0:
            return None
        id, row, column, time, resources = last_observation[0]
        return ((row, column), time, resources)

    def get_all_info_from_agent(
        self, other_id
    ) -> List[Tuple[Tuple[int, int], int, int]]:
        """Devuelve toda la informacion recolectada sobre las apariciones de
        un agente cuyo id fue provisto\n
        Cada aparicion es expresada como una tupla que contiene la posicion donde fue visto
        el agente, la iteracion en que ocurrio la observacion y la cantidad de azucar que
        llevaba"""
        observations = self.cursor.execute(
            QUERY_FOR_ALL_APPEARENCES_OF_AGENT % (self.table_name, str(other_id))
        ).fetchall()
        answer = [
            ((row, column), time, resources)
            for id, row, column, time, resources in observations
        ]
        return answer

    def get_last_info_of_position(
        self, row: int, column: int
    ) -> Tuple[int, Tuple[int, int] | None]:
        """Dadas las coordenadas de una posicion, retorna la ultima informacion recolectada
        sobre esa posicion.\n Tal informacion es expresada como una tupla que contiene como
        primer componente la iteracion en que ocurrio la observacion y como segundo None en
        caso de que la casilla estuviera vacia en el momento de realizar la observacion o
        una tupla con el id del agente observado y la cantidad de azucar que llevaba\n
        Si no hay informacion en lo absoluto sobre la casilla retorna None"""
        last_observation = self.cursor.execute(
            QUERY_FOR_LAST_APPEARENCE_IN_A_POSITION
            % (self.table_name, str(row), str(column))
        ).fetchall()
        if len(last_observation) == 0:
            return None
        id, row, column, time, resources = last_observation[0]
        if id:
            return (time, (id, resources))
        else:
            return (time, None)

    def get_all_info_of_position(
        self, row: int, column: int
    ) -> List[Tuple[int, Tuple[int, int] | None]]:
        """Dadas las coordenadas de una posicion, retorna toda la informacion recolectada a lo
        largo de la simulacion acerca de esa posicion.\n
        El valor de retorno es una lista de tuplas, donde cada tupla corresponde a una observacion
        de la posicion. Cada tupla tiene por primer componente el momento en que ocurrio la
        observacion y como segundo, una tupla con el id del agente observado y la cantidad de
        azucar que llevaba, o None en caso de que no hubiera ningun agente en la posicion en
        ese momento"""
        observations = self.cursor.execute(
            QUERY_FOR_ALL_APPEARENCES_IN_A_POSITION
            % (self.table_name, str(row), str(column))
        )
        answer = [
            (iteration, (id, resources))
            for id, row, column, iteration, resources in observations
        ]
        return answer

    def get_last_observation_of_each_agent(
        self,
    ) -> Dict[int, Tuple[Tuple[int, int], int, int]]:
        """Devuelve la ultima observacion que se tuvo de cada agente como un diccionario donde al
        id del agente se le hace corresponder la observacion\n
        Cada observacion aparec expresada como una tupla cuyo primer componente es la posicion donde
        se encontraba el agente, el segundo la iteracion en que se produjo la observacion y el
        tercero es la cantidad de azucar que llevaba con sigo"""
        answer = {}
        for agent_id in self.agents_seen:
            answer[agent_id] = self.get_last_info_from_agent(agent_id)
        return answer


# conn = sqlite3.connect(':memory:')
# m = Memory_for_Agents_Sights(3, conn)
# cursor = m.add_appearence(1, (0, 0), 0, 0)
# print(m.get_last_info_from_agent(1))
# print(m.get_all_info_from_agent(1))
# print(m.get_last_info_of_position(0, 0))
# print(m.get_all_info_of_position(0, 0))
