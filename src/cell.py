from __future__ import annotations
import enum

from line import Line
from point import Direction, Point
from window import Window


class Wall(enum.IntEnum):
    EAST_WALL = 1 << 0
    NORTH_WALL = 1 << 1
    WEST_WALL = 1 << 2
    SOUTH_WALL = 1 << 3

    def opposite(self) -> Wall:
        left = 0b1111 << 4
        right = 0b1111
        w = self << 2
        w = ((w & left) >> 4) | (w & right)
        return Wall(w)

    @staticmethod
    def from_direction(d: Direction):
        match d:
            case Direction.NORTH:
                return Wall.NORTH_WALL
            case Direction.SOUTH:
                return Wall.SOUTH_WALL
            case Direction.WEST:
                return Wall.WEST_WALL
            case Direction.EAST:
                return Wall.EAST_WALL

    def to_direction(self):
        match (self):
            case Wall.NORTH_WALL:
                return Direction.NORTH
            case Wall.EAST_WALL:
                return Direction.EAST
            case Wall.WEST_WALL:
                return Direction.WEST
            case Wall.SOUTH_WALL:
                return Direction.SOUTH


ALL_WALLS = Wall.EAST_WALL | Wall.SOUTH_WALL | Wall.WEST_WALL | Wall.NORTH_WALL


class Cell:
    def __init__(self, top_left: Point, bottom_right: Point):
        self._top = top_left.y
        self._left = top_left.x
        self._bot = bottom_right.y
        self._right = bottom_right.x
        self._walls = ALL_WALLS
        self._visited = False

    def __repr__(self):
        return f"Cell: ({self._left}, {self._top}) ({self._right}, {self._bot}): Walls: {self._walls}"

    def middle(self):
        return Point((self._left + self._right) // 2, (self._top + self._bot) // 2)

    def wall_line(self, wall: Wall):
        match wall:
            case Wall.EAST_WALL:
                p1 = Point(self._right, self._top)
                p2 = Point(self._right, self._bot)
            case Wall.WEST_WALL:
                p1 = Point(self._left, self._top)
                p2 = Point(self._left, self._bot)
            case Wall.NORTH_WALL:
                p1 = Point(self._left, self._top)
                p2 = Point(self._right, self._top)
            case Wall.SOUTH_WALL:
                p1 = Point(self._left, self._bot)
                p2 = Point(self._right, self._bot)
            case _:
                assert False

        return Line(p1, p2)

    def wall_check(self, wall: Wall):
        return (self._walls & wall) > 0

    def wall_set(self, wall: Wall):
        self._walls |= int(wall)

    def wall_remove(self, wall: Wall):
        mask = ~(ALL_WALLS & wall)
        self._walls &= mask

    def wall_toggle(self, wall: Wall):
        if self.wall_check(wall):
            self.wall_remove(wall)
        else:
            self.wall_set(wall)

    def draw(self, window: Window):
        for wall in [
            Wall.EAST_WALL,
            Wall.NORTH_WALL,
            Wall.WEST_WALL,
            Wall.SOUTH_WALL,
        ]:
            line = self.wall_line(wall)
            if self.wall_check(wall):
                window.draw_line(line, "black")
            else:
                window.draw_line(line, window._root["bg"])

    def draw_move(self, window: Window, dest: Cell, undo: bool = False):
        col = "gray" if undo else "red"
        line = Line(self.middle(), dest.middle())
        window.draw_line(line, col)
