from __future__ import annotations
import enum

from line import Line
from point import Point
from window import Window


class Wall(enum.IntEnum):
    EAST_WALL = 1 << 0
    NORTH_WALL = 1 << 1
    WEST_WALL = 1 << 2
    SOUTH_WALL = 1 << 3


class Cell:
    def __init__(self, top_left: Point, bottom_right: Point):
        self._top = top_left.y
        self._left = top_left.x
        self._bot = bottom_right.y
        self._right = bottom_right.x
        self._walls = 0

    def __repr__(self):
        return f"Cell: ({self._left}, {self._top}) ({self._right}, {self._bot}): Walls: {self._walls}"

    def middle(self):
        return Point((self._left + self._right) / 2, (self._top + self._bot) / 2)

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

        return Line(p1, p2)

    def wall_check(self, wall: Wall):
        return (self._walls & int(wall)) > 0

    def wall_set(self, wall: Wall):
        self._walls |= int(wall)

    def draw(self, window: Window):
        for wall in [
            Wall.EAST_WALL,
            Wall.NORTH_WALL,
            Wall.WEST_WALL,
            Wall.SOUTH_WALL,
        ]:
            if self.wall_check(wall):
                line = self.wall_line(wall)
                window.draw_line(line, "black")

    def draw_move(self, window: Window, dest: Cell, undo: bool = False):
        col = "gray" if undo else "red"
        line = Line(self.middle(), dest.middle())
        window.draw_line(line, col)
