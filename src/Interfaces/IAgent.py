from abc import ABC, abstractmethod


class IAgent(ABC):
    @abstractmethod
    def move(self, dx, dy):
        """Mueve el agente a una nueva posición."""
        pass

    @abstractmethod
    def interact(self, other):
        """Define la interacción con otro agente."""
        pass

    @abstractmethod
    def heuristic(self):
        """Aplica una heurística para tomar decisiones."""
        pass

    @abstractmethod
    def decide_next_move(self):
        """Decide el siguiente movimiento."""
        pass

    @abstractmethod
    def decide_interaction(self):
        """Decide si interactuar o no."""
        pass
