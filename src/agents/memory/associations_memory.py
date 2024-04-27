import sqlite3
from typing import List, Set, Tuple, Dict
CREATE_TABLE = """CREATE TABLE %s (agent_id INTEGER, association_id INTEGER, duty INTEGER,
    reward INTEGER)"""
INSERT_MEMBRESY = """INSERT INTO %s (agent_id, association_id, duty, reward) VALUES(%s, %s, %s, %s);"""
QUERY_FOR_AGENT_MEMBRESIES = """SELECT * FROM %s WHERE agent_id = %s"""
QUERY_FOR_MEMBERS_OF_ASSOCIATION = """SELECT * FROM %s WHERE association_id = %s"""

class Associations_Memory:
    def __init__(self, id : int, conn : sqlite3.Connection):
        """Esta clase maneja la memoria del agente relativa a las asociaciones cuya existencia
        conoce."""
        self.id = id
        self.cursor = conn.cursor()
        self.table_name = "associations_" + str(self.id)
        self.cursor = self.cursor.execute(CREATE_TABLE%(self.table_name))
        self.association_creation_time : Dict[int, int] = {}
    
    def add_association(self, association_id : int, member_ids : Set[int], commitments : Dict[int, Tuple[int, int]], iteration : int):
        """Anhade a la base de datos toda la informacion relativa a una asociacion\n
        Primeramente comprueba si ya la asociacion esta registrada, en cuyo caso termina
        el metodo para evitar insertar entradas duplicadas en la tabla. De no haber sido
        registrada anteriormente, guarda el numero de la iteracion en que se registro\n
        Cada asociacion es registrada en la tabla de la siguiente manera:\n
        Para cada uno de sus miembros crea una entrada con el id del miembro, el id de la 
        asociacion, el duty (primera componente del commitment, o sea, la porcion de sus 
        ganancias que el agente debe entregar a la asociacion) y el reward (segunda componente
        del commitment, o sea, la porcion de la recaudacion de la asociacion que corresponde
        al agente)\n"""
        for member_id in member_ids:
            duty, reward = commitments[member_id]
            self.cursor = self.cursor.execute(INSERT_MEMBRESY%(self.table_name, member_id, association_id, str(duty), str(reward)))
        return self.cursor
    
    def get_all_associations_of_agent(self, agent_id : int) -> List[Tuple[int, Tuple[int, int]]]:
        """Dado el id de un agente, retorna todas las asociaciones a las que pertenece\n
        Cada asociacion es descrita como una tupla con el id de la asociacion y su commitment
        con la asociacion"""
        membresies = self.cursor.execute(QUERY_FOR_AGENT_MEMBRESIES%(self.table_name, str(agent_id))).fetchall()
        answer = []
        for _, association_id, duty, reward in membresies:
            answer.append((association_id, (duty, reward)))
        return answer
    
    def get_all_members_of_associations(self, association_id : int) -> List[Tuple[int, Tuple[int, int]]]:
        """Dado el id de una asociacion, retorna una lista con todos sus miembros\n
        Cada miembro es descrito como una tupla con su id y su commitment"""
        members = self.cursor.execute(QUERY_FOR_MEMBERS_OF_ASSOCIATION%(self.table_name, str(association_id)))
        answer = []
        for member_id, _, duty, reward in members:
            answer.append(member_id, (duty, reward))
        return answer