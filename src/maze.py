from cell import Cell, Wall
import random
from point import Direction, Point
from window import Window
from typing import Optional
from time import sleep


class Maze:
    def __init__(
        self,
        window: Optional[Window],
        top_left: Point,
        n_rows: int,
        n_cols: int,
        cell_width: int,
        cell_height: int,
        seed: Optional[int] = None,
        speed: float = 0.05,
    ):
        self.win = window
        self._top_left = top_left
        self._num_rows = n_rows
        self._num_cols = n_cols
        self._cell_width = cell_width
        self._cell_height = cell_height
        self._speed = speed
        if seed:
            random.seed(seed)

        self._cells: list[list[Cell]] = Maze._create_cells(
            top_left, n_rows, n_cols, cell_width, cell_height
        )

    def _unset_visited(self):
        for row in self._cells:
            for cell in row:
                cell._visited = False

    def _break_walls(self, point: Point):
        self._cells[point.x][point.y]._visited = True
        while True:
            outs = []
            for direction in [
                Direction.NORTH,
                Direction.EAST,
                Direction.SOUTH,
                Direction.WEST,
            ]:
                neighbor = point.move(direction)
                if (
                    False
                    or neighbor.x < 0
                    or neighbor.y < 0
                    or neighbor.y >= len(self._cells)
                    or neighbor.x >= len(self._cells[neighbor.y])
                ):
                    continue
                if self._cells[neighbor.x][neighbor.y]._visited:
                    continue
                outs.append(direction)

            if not outs:
                self._draw_cell(point)
                return
            out = outs[random.randint(0, len(outs) - 1)]

            self.remove_wall(point.x, point.y, Wall.from_direction(out))
            self._break_walls(point.move(out))

    def draw_cells(self):
        if not self.win:
            print("Maze has no window")
            return
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self._draw_cell(Point(i, j))

    def break_entrance_and_exit(self):
        assert self._cells
        self._cells[0][0].wall_remove(Wall.NORTH_WALL)
        self._cells[-1][-1].wall_remove(Wall.SOUTH_WALL)

    @staticmethod
    def _create_cells(top_left: Point, num_rows, num_cols, cell_width, cell_height):
        cells = []
        tl_y = top_left.y
        for _ in range(num_rows):
            tl_x = top_left.x
            row = []
            for _ in range(num_cols):
                c_top_left = Point(tl_x, tl_y)
                c_bot_right = Point(
                    tl_x + cell_width,
                    tl_y + cell_height,
                )
                c = Cell(c_top_left, c_bot_right)
                row.append(c)
                tl_x += cell_width

            cells.append(row)
            tl_y += cell_height

        return cells

    def remove_wall(self, row: int, col: int, wall: Wall):
        cell = self._cells[row][col]
        cell.wall_remove(wall)
        match wall:
            case Wall.EAST_WALL:
                neighbor = (row, col + 1)
            case Wall.WEST_WALL:
                neighbor = (row, col - 1)
            case Wall.SOUTH_WALL:
                neighbor = (row + 1, col)
            case Wall.NORTH_WALL:
                neighbor = (row - 1, col)
        if neighbor[0] < len(self._cells):
            cell_row = self._cells[neighbor[0]]
            if neighbor[1] < len(cell_row):
                cell = cell_row[neighbor[1]]
                wall = wall.opposite()
                cell.wall_remove(wall)

    def _draw_cell(self, xy: Point):
        if self.win:
            self._cells[xy.x][xy.y].draw(self.win)
            self._animate()

    def _animate(self):
        if not self.win:
            return
        self.win.redraw()
        sleep(self._speed)
