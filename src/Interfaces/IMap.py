from abc import ABC, abstractmethod
from typing import Tuple


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
    def move(self, sx, sy, dx, dy):
        pass

    @abstractmethod
    def peek_from(self, x, y, vision_range):
        pass

    @abstractmethod
    def shot(self, agent_id : str, direction : Tuple[int, int], max_length : int):
        pass