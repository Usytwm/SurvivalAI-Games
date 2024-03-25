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
