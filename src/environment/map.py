import bidict
from typing import Tuple
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__terrain__ = bidict.bidict()
    
    def IsValid(self, position : Tuple[int, int]):
        return (position[0] >= 0) and (position[0] < self.height) and (position[1] >= 0) and (position[1] < self.width)
    
    def insert(self, position : Tuple[int, int], id : int) -> None:
        "Inserts in a given position an element with the given id"
        if self.IsValid(position):
            if self.__terrain__.get(position, None):
                raise PositionTaken
            try:
                self.__terrain__[position] = id
                return
            except:
                raise IDAlreadyExists
        raise NotValidPosition

    def pop_from_position(self, position : Tuple[int, int]) -> int | None:
        """Remove the element at the given position, and returns its id, or None if there is
        no element at the position"""
        if self.IsValid(position):
            try:
                return self.__terrain__.pop(position)
            except:
                return None
        raise NotValidPosition
    
    def pop_id(self, id : int) -> Tuple[int, int]:
        "Removes the element with the given id and returns its position"
        try:
            return self.__terrain__.inverse.pop(id)
        except:
            raise IDDoesntExists
    
    def peek_from_position(self, position : Tuple[int, int]) -> int | None:
        "If there is an element in the given position returns it, otherwise returns None"
        if self.IsValid(position):
            try:
                return self.__terrain__[position]
            except:
                return None
        raise NotValidPosition
    
    def peek_id(self, id : int) -> Tuple[int, int]:
        "Returns the position of an element with the given id"
        try:
            return self.__terrain__.inverse[id]
        except:
            raise IDDoesntExists
    
    def move(self, id : int, new_position : Tuple[int, int]):
        "Moves the element with the given id to a new position"
        self.pop_id(id)
        self.insert(new_position, id)


class MapException(Exception):
    pass

class PositionTaken(MapException):
    pass

class IDAlreadyExists(MapException):
    pass

class NotValidPosition(MapException):
    pass

class IDDoesntExists(MapException):
    pass