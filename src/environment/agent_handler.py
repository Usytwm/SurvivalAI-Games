from typing import Tuple, Dict, List, Set
from Interfaces.IAgent import IAgent
from Interfaces.IRange import IRange
from Interfaces.IMovement import IMovement
from Interfaces.IVision import IVision
from Interfaces.IAttack_Range import IAttackRange
from map import Map
from sim_object import Sim_Object, Sim_Object_Type
from actions import Action_Info, Action, Attack, Association_Proposal
from association import Association


class Agent_Handler(Sim_Object):
    def __init__(
        self,
        id: int,
        reserve: int,
        consume: int,
        map: Map,
        agent: IAgent,
        movement: IMovement,
        vision: IVision,
        attack_range: IAttackRange,
    ):
        super().__init__(id, Sim_Object_Type.AGENT, reserve)
        self.reserve = reserve
        self.consume = consume
        self.map = map
        self.agent = agent
        self.movement = movement
        self.vision = vision
        self.attack_range = attack_range
        self.associations: Dict[int, Association] = {}
        self.free_portion = 1
        self.partners: Dict[int, int] = {}
        #partners contiene para cada aliado, cuantas asociaciones este agente comparte con tal aliado
        #de manera que podemos saber si sigue siendo aliado tras eliminar una de esas asociaciones
        #o no

    @property
    def IsDead(self):
        return self.reserve < 0

    @property
    def IsAssociated(self):
        return len(self.associations) > 0

    def move(self) -> Tuple[int, int]:
        """Devuelve el movimiento que desea realizar el agente este turno de ser valido.\n
        El movimiento es expresado como una tupla que representa el movimiento en la posicion
        horizontal y en la vertical respectivamente, por ejemplo (-1, 3) representa que se
        movio una fila hacia arriba y tres columnas a la derecha\n
        Si el movimiento elegido por el agente no fuera valido devuelve (0, 0)"""
        possible_moves = self.movement.moves(self.map, self.id)
        move = self.agent.move()
        return move if move in possible_moves else (0, 0)

    def inform_move(self, movement: Tuple[int, int]) -> None:
        "Informs the agent he has moved to the given position"
        return self.agent.inform_move(movement)

    def get_attacks(self) -> List[Attack]:
        """Get the attacks that the agent wants to make in this turn, and returns only the
        valid ones"""
        attacks: List[Attack] = self.agent.get_attacks()
        possible_victims = set(self.attack_range.possible_victims(self.map, self.id))
        sum_of_attacks = 0  # Verificamos ademas, que el agente no gaste mas en ataques de lo que puede gastar
        confirmed_attacks = []
        for attack in attacks:
            victim = attack.destinataries_ids[0]
            if (
                not (victim in possible_victims)
                or (victim in self.partners)
                or (victim == self.id)
            ):
                # no puede atacar a un socio o a alguien fuera de su rango o a si mismo
                continue
            confirmed_attacks.append(attack)
            sum_of_attacks += attack.strength
        if sum_of_attacks > self.reserve:
            # Si hizo mas ataques de los que puede pagar, no le aceptamos ninguno
            confirmed_attacks = []
        return confirmed_attacks

    def get_association_proposals(self) -> List[Association_Proposal]:
        """Get the association proposals the agent wants to make in this turn and returns only
        the valid ones"""
        # TODOf Insertar comprobaciones de que la propuesta tiene sentido
        return self.agent.get_association_proposals()
    
    def consider_association_proposal(self, proposal : Association_Proposal) -> bool:
        "Consulta al agente si desea o no ser miembro de la asociacion y retorna su respuesta"
        return self.agent.consider_association_proposal(proposal)

    def inform_of_attack_made(self, victim_id: int, strength: int) -> None:
        "Informs the agent that an attack that he has requested, has been executed"
        self.reserve -= strength
        return self.agent.inform_of_attack_made(victim_id, strength)

    def inform_of_attack_received(self, attacker_id: int, strength: int) -> None:
        "Informs the agent of an attack he has received"
        self.reserve -= strength
        position_attack_recived = self.map.peek_id(attacker_id)
        return_value = self.agent.inform_of_attack_received(
            attacker_id, strength, position_attack_recived
        )
        return return_value
    
    def inform_joined_association(self, association : Association):
        "Informa al agente que se ha unido a una asociacion"
        self.associations[association.id] = association
        self.free_portion = self.free_portion - association.commitments[self.id][0]
        for agent_id in association.members:
            if agent_id != self.id:
                self.partners[agent_id] = self.partners.get(agent_id, 0) + 1
        self.agent.inform_joined_association(association.id, association.members, association.commitments)
    
    def inform_broken_association(self, association_id : int):
        "Informa al agente que se ha roto una asociacion a la que pertenece"
        self.free_portion = self.free_portion + self.associations[association_id].commitments[self.id][0]
        for agent_id in self.associations[association_id].members:
            if agent_id != self.id:
                self.partners[agent_id] -= 1
                if self.partners[agent_id] == 0:
                    self.partners.pop(agent_id)
        self.associations.pop(association_id)
        self.agent.inform_broken_association(association_id)

    def take_attack_reward(self, victim_id: int, reward: int):
        """Informs the agent of the reward obtained by killing an agent, and actualizes
        its reserves"""
        self.reserve += reward
        return self.agent.take_attack_reward(victim_id, reward)

    def see_objects(self, objects: Dict[int, Sim_Object]) -> None:
        "Loads the objects the agent can see in this turn, and sends it to him"
        vision = self.vision.see_objects(self.map, self.id, objects)
        self.agent.see_objects(vision)
        # print("Agent " + str(self.id) + " sees: " + str(vision))

    def see_resources(self) -> None:
        """Loads the info about the resources in the positions the agent can see in this turn
        and sends it to him"""
        # Solo puede ver cuanta azucar hay en las casillas que no estan ocupadas
        vision = self.vision.see_resources(self.map, self.id)
        self.agent.see_resources(vision)

    def see_actions(self) -> None:
        "Loads the info about events that had occured in the agents sight"
        vision = self.vision.see_actions(self.map, self.id)
        self.agent.see_actions(vision)

    def feed(self, sugar: int) -> None:
        """Increaes the agent reserves with the amount of sugar given, and informs the agent"""
        self.reserve = self.reserve + sugar
        self.agent.feed(
            sugar
        )
    def burn(self) -> None:
        """Dimishes the agent reserves by his diary consume."""
        self.reserve = self.reserve - self.consume
        self.agent.burn()
