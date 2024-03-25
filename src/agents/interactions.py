from Interfaces.IAgent import IAgent


class InteractionType:
    ATTACK = "attack"
    TRADE = "trade"
    ALLIANCE = "alliance"


class InteractionEvent:
    def __init__(self, type, initiator, target, data=None):
        self.type = type
        self.initiator = initiator
        self.target = target
        self.data = data  # Información adicional, p.ej., objetos a intercambiar


class AgentInteractionManager:

    def interact(self, interaction_event):
        if interaction_event.type == InteractionType.ATTACK:
            self.handle_attack(interaction_event)
        elif interaction_event.type == InteractionType.TRADE:
            self.handle_trade(interaction_event)
        elif interaction_event.type == InteractionType.ALLIANCE:
            self.handle_alliance(interaction_event)

    def handle_attack(self, interaction_event: InteractionEvent):
        # Lógica específica para manejar un ataque
        # aki pueod poner que en cada usuario queataque el otro se defienda esto lo haria
        # teninado un metodo defense en los usuarios que se utiliza cuando alguien te sta aacanco
        # ntonces pasaria target.defense(initiator.attack) y en el metodo defense de cada usuario
        # se modelaria de tal manera que el que se defiende decida si contaatacar o defendercesolamente, o realizar aguna otra accion
        print(
            f"{interaction_event.initiator.name} ataca a {interaction_event.target.name}"
        )

    def handle_trade(self, interaction_event):
        # Lógica específica para manejar un intercambio, yo te doy algo tu me das algo que segun alguna heuristica manehe cada agente
        print(
            f"{interaction_event.initiator.name} intercambia con {interaction_event.target.name}"
        )

    def handle_alliance(self, interaction_event):
        # Lógica específica para formar una alianza
        # esto teine que ser simetrico si uno forma alianza con otro el otro tambien tiene que formar alianza con el uno
        # ademas de tener algo en cada ajete que indique si tiene alianza con otro agente para poder realizar acciones
        # en conjunto con el otro agente o romper la alianza seu=gun losmparamtros que decida
        print(
            f"{interaction_event.initiator.name} forma una alianza con {interaction_event.target.name}"
        )
