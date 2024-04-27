import sqlite3
from typing import Dict, List, Tuple

CREATE_TABLE = """CREATE TABLE %s (attacker_id INTEGER, victim_id INTEGER,
iteration INTEGER)"""
INSERT_ATTACK = """INSERT INTO %s (attacker_id, victim_id, iteration, strength) VALUES(%s, %s, %s, %s)"""
QUERY_FOR_ALL_ATTACKS_MADE = """SELECT * FROM %s WHERE attacker_id = %s ORDER BY iteration DESC"""
QUERY_FOR_LAST_ATTACK_MADE = """SELECT * FROM %s WHERE attacker_id = %s ORDER BY iteration DESC LIMIT 1"""
QUERY_FOR_ATTACKS_MADE_IN_A_TURN = """SELECT * FROM %s WHERE attacker_id = %s AND iteration = %s"""
QUERY_FOR_ALL_ATTACKS_RECEIVED = """SELECT * FROM %s WHERE victim_id = %s ORDER BY iteration DESC"""
QUERY_FOR_LAST_ATTACK_RECEIVED = """SELECT * FROM %s WHERE victim_id = %s ORDER BY iteration DESC LIMIT 1"""
QUERY_FOR_ATTACKS_RECEIVED_IN_A_TURN = """SELECT * FROM %s WHERE victim_id = %s AND iteration = %s"""

class Memory_for_Attacks:
    def __init__(self, id : int, conn : sqlite3.Connection):
        self.id = id
        self.cursor = conn.cursor()
        self.table_name = "attacks_" + str(self.id)
        self.deaths : Dict[int, int] = {}
        self.cursor = self.cursor.execute(CREATE_TABLE%(self.table_name))
    
    def add_attack(self, attacker_id : int, victim_id : int, iteration : int, strength : int):
        self.cursor = self.cursor.execute(INSERT_ATTACK%(attacker_id, victim_id, iteration, strength))
    
    def add_death(self, dead_id, iteration):
        self.deaths[dead_id] = iteration
    
    def get_last_attack_of_agent(self, id : int) -> Tuple[int, int, int]:
        """Dado el id de un agente devuelve una tupla con el instante de tiempo en que ataco
        por ultima vez, el id de la victima de su ataque y la fuerza del ataque"""
        last_attack = self.cursor.execute(QUERY_FOR_LAST_ATTACK_MADE%(self.table_name, id)).fetchall()
        if len(last_attack) == 0:
            return None
        attacker_id, victim_id, iteration, strength = last_attack[0]
        return (iteration, victim_id, strength)

    def get_attack_of_agent_in_a_turn(self, id : int, iteration : int) -> List[Tuple[int, int]]:
        """Dado un id y un instante de tiempo, devuelve los ataques realizados por el agente
        cuyo id fue provisto en el instante de tiempo provisto. Cada ataque es expresado como
        una tupla (victim_id, strength)"""
        attacks = self.cursor.execute(QUERY_FOR_ATTACKS_MADE_IN_A_TURN%(self.table_name, id)).fetchall()
        return [(victim_id, strength) for attacker_id, victim_id, iteration, strength in attacks]

    def get_attacks_of_agent(self, id : int) -> List[Tuple[int, Tuple[int, int]]]:
        """Dado el id de un agente, devuelve todos los ataques realizados por este, expresados
        como tuplas cuyo primer componente es la iteracion en que ocurrio el ataque y su
        segundo componente es una tupla con el id de la victima y la fuerza del ataque"""
        attacks = self.cursor.execute(QUERY_FOR_ALL_ATTACKS_MADE%(self.table_name, id)).fetchall()
        return [(iteration, (victim_id, strength)) for attacker_id, victim_id, iteration, strength in attacks]

    def get_all_attacks_against_agent_in_a_turn(self, id : int) -> List[Tuple[int, int]]:
        """Dado el id de un agente y una iteracion devuelve una lista con todos los
        ataques realizados contra el agente en tal iteracion, cada ataque expresado como una tupla
        atacante, fortaleza"""
        attacks = self.cursor.execute(QUERY_FOR_ATTACKS_RECEIVED_IN_A_TURN%(self.table_name, id)).fetchall()
        return [(attacker_id, strength) for attacker_id, victim_id, iteration, strength in attacks]

    def get_all_attacks_against_agent(self, id : int):
        """Dado el id de un agente devuelve una lista con todos los ataques realizados en su
        contra. Los ataques aparecen expresados como tuplas cuyo primer componente es la iteracion
        en que ocurrio el ataque y su segundo es una tupla con el id del atacante y la fuerza del
        ataque"""
        attacks = self.cursor.execute(QUERY_FOR_ALL_ATTACKS_RECEIVED%(self.table_name, id)).fetchall()
        return [(iteration, (attacker_id, strength)) for attacker_id, victim_id, iteration, strength in attacks]

    def get_last_attack_against_agent(self, id : int):
        """Dado el id de un agente devuelve cual fue el ultimo ataque realizado contra el
        como una tupla instante de tiempo, atacante, fuerza"""
        last_attack = self.cursor.execute(QUERY_FOR_LAST_ATTACK_RECEIVED%(self.table_name, id)).fetchall()
        if len(last_attack) == 0:
            return None
        attacker_id, victim_id, iteration, strength = last_attack[0]
        return (iteration, attacker_id, strength)

    def get_time_of_death(self, id : int):
        """Dado el id de un agente devuelve cual fue el turno de su muerte"""
        return self.deaths[id]