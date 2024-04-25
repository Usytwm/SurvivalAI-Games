import sqlite3
from typing import Tuple, List

CREATE_TABLE = """CREATE TABLE %s (agent_id INTEGER, row INTEGER, column INTEGER,
iteration INTEGER, resources INTEGER)"""
INSERT_APPEARENCE = """INSERT INTO %s (agent_id, row, column, iteration, resources) VALUES(%s, %s, %s, %s, %s);"""
SELECT_QUERY = """SELECT * FROM %s"""
QUERY_FOR_LAST_APPEARENCE = """SELECT * FROM %s WHERE agent_id = %s ORDER BY iteration DESC LIMIT 1"""
QUERY_FOR_ALL_APPEARENCES = """SELECT * FROM %s WHERE agent_id = %s ORDER BY iteration DESC"""


class Memory_for_Agents_Sights:
    """Una instancia de esta clase corresponde a la memoria que tiene un agente acerca de
    donde, cuando y como ha observado a otros agentes\n
    Esta clase funciona accediendo a una tabla de sqlite guardada en memoria (no es persistente)\n
    Cada fila de la tabla describe la observacion de otro agente por parte del agente cuya
    memoria estamos controlando. Tal observacion es descrita usando el id del agente observado
    la posicion en que fue observado, la fecha en que fue observado, la cantidad de azucar que
    traia consigo asi como otros detalles que se puedan ir incluyendo.
    """

    def __init__(self, id, conn : sqlite3.Connection):
        """Para instanciar esta clase necesitamos el id del agente cuya memoria sera controlada
        por la instancia\n. En este metodo ademas creamos la tabla asociada a este agente
        y por ello en el momento de instanciar necesitamos la conexion donde se creara esa tabla"""
        self.id = id
        self.cursor = conn.cursor()
        self.table_name = "agents_sights_" + str(self.id)
        self.cursor = self.cursor.execute(CREATE_TABLE%(self.table_name))
    
    def add_appearence(self, other_id : int, position : Tuple[int, int], iteration : int, resources : int):
        return self.cursor.execute(INSERT_APPEARENCE%(self.table_name, other_id, position[0], position[1], iteration, resources))

    def get_last_info_from_agent(self, other_id) -> Tuple[Tuple[int, int], int, int]:
        """Devuelve la ultima informacion recolectada sobre el agente cuyo id fue provisto.\n
        El valor de devuelto es una tupla que contiene la posicion donde estaba como primer
        componente, el momento en que fue visto como segunda componente
        y la cantidad de azucar que llevaba como tercero\n
        Returna None si no ha visto al agente"""
        last_observation = self.cursor.execute(QUERY_FOR_LAST_APPEARENCE%(self.table_name, str(other_id))).fetchall()
        if len(last_observation) == 0:
            return None
        id, row, column, time, resources = last_observation[0]
        return ((row, column), time, resources)
    
    def get_all_info_from_agent(self, other_id) -> List[Tuple[Tuple[int, int], int, int]]:
        """Devuelve toda la informacion recolectada sobre las apariciones de 
        un agente cuyo id fue provisto\n
        Cada aparicion es expresada como una tupla que contiene la posicion donde fue visto
        el agente, la iteracion en que ocurrio la observacion y la cantidad de azucar que
        llevaba"""
        observations = self.cursor.execute(QUERY_FOR_ALL_APPEARENCES%(self.table_name, str(other_id))).fetchall()
        if len(observations) == 0:
            return None
        answer = [((row, column), time, resources) for id, row, column, time, resources in observations]
        return answer

#conn = sqlite3.connect(':memory:')
#m = Memory_for_Agents_Sights(3, conn)
#cursor = m.add_appearence(1, (0, 0), 0, 0)
#print(m.get_last_info_from_agent(1))
#print(m.get_all_info_from_agent(1))