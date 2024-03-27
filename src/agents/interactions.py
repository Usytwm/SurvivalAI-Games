from Interfaces.IAgent import IAgent


class InteractionType:
    ATTACK = "attack"
    TRADE = "trade"
    ALLIANCE = "alliance"
    DEFEND = "defend"


class InteractionEvent:
    def __init__(self, type, initiator: IAgent, target: IAgent, map=None, data=None):
        self.type = type
        self.initiator = initiator
        self.target = target
        self.data = data
        self.map = map


class AgentInteractionManager:

    def interact(self, interaction_event):
        if interaction_event.type == InteractionType.ATTACK:
            self.handle_attack(interaction_event)
        elif interaction_event.type == InteractionType.TRADE:
            self.handle_trade(interaction_event)
        elif interaction_event.type == InteractionType.ALLIANCE:
            self.handle_alliance(interaction_event)
        elif interaction_event.type == InteractionType.DEFEND:
            self.handle_defend(interaction_event)

    def handle_attack(self, interaction_event: InteractionEvent):
        interaction_event.initiator.attack(interaction_event.target)

    def handle_defend(self, interaction_event: InteractionEvent):
        interaction_event.initiator.defend(
            interaction_event.data, interaction_event.target
        )

    def handle_trade(self, interaction_event):
        # Lógica específica para manejar un intercambio, yo te doy algo tu me das algo que segun alguna heuristica manehe cada agente
        print(
            f"{interaction_event.initiator.name} intercambia con {interaction_event.target.name}"
        )

    def handle_alliance(self, interaction_event):
        interaction_event.initiator.add_ally(interaction_event.target.name)
        interaction_event.target.add_ally(interaction_event.initiator.name)
