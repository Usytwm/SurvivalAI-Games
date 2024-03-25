from abc import ABC, abstractmethod


class IMapInfoProvider(ABC):
    @abstractmethod
    def valid_position(self, x, y) -> bool:
        pass

    @abstractmethod
    def cell_content(self, x: int, y: int):
        pass

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def request_move(self, agent, dx, dy):
        pass
