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
        i = self.x
        j = self.y
        match direction:
            case Direction.NORTH:
                return Point(i - 1, j)
            case Direction.EAST:
                return Point(i, j + 1)
            case Direction.SOUTH:
                return Point(i + 1, j)
            case Direction.WEST:
                return Point(i, j - 1)
