from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def move(self, direction: Direction):
        x = self.x
        y = self.y
        match direction:
            case Direction.NORTH:
                return Point(x, y + 1)
            case Direction.EAST:
                return Point(x + 1, y)
            case Direction.SOUTH:
                return Point(x, y - 1)
            case Direction.WEST:
                return Point(x - 1, y)
