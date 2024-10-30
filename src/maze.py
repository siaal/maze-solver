from cell import Cell, Wall
import random
from point import Direction, Point
from stack import Stack
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
        self.speed = speed
        if seed:
            random.seed(seed)

        self._cells: list[list[Cell]] = Maze._create_cells(
            top_left, n_rows, n_cols, cell_width, cell_height
        )

    @property
    def entrance_point(self):
        return Point(0, self._num_rows - 1)

    @property
    def exit_point(self):
        return Point(self._num_cols - 1, 0)

    def _unset_visited(self):
        for row in self._cells:
            for cell in row:
                cell._visited = False

    def _cell(self, p: Point) -> Optional[Cell]:
        if 0 <= p.y < self._num_rows and 0 <= p.x < self._num_cols:
            return self._cells[p.y][p.x]
        return None

    def _break_walls(self, point: Point):
        cell = self._cell(point)
        assert cell
        cell._visited = True
        while True:
            outs = []
            for direction in [
                Direction.NORTH,
                Direction.EAST,
                Direction.SOUTH,
                Direction.WEST,
            ]:
                neighbor = self._cell(point.move(direction))
                if not neighbor or neighbor._visited:
                    continue
                outs.append(direction)

            if not outs:
                self._draw_cell(point)
                return

            out = outs[random.randint(0, len(outs) - 1)]
            self.remove_wall(point, Wall.from_direction(out))
            self._break_walls(point.move(out))

    def draw_cells(self):
        if not self.win:
            print("Maze has no window")
            return
        for y in range(self._num_rows):
            for x in range(self._num_cols):
                self._draw_cell(Point(x, y))

    def break_entrance_and_exit(self):
        assert self._cells
        entrance = self._cell(self.entrance_point)
        assert entrance
        entrance.wall_remove(Wall.NORTH_WALL)
        self._draw_cell_direct(entrance)
        ex = self._cell(self.exit_point)
        assert ex
        ex.wall_remove(Wall.SOUTH_WALL)
        self._draw_cell_direct(ex)

    @staticmethod
    def _create_cells(top_left: Point, num_rows, num_cols, cell_width, cell_height):
        cells = []
        tl_y = top_left.y + ((num_rows - 1) * cell_height)
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
            tl_y -= cell_height

        return cells

    def remove_wall(self, point: Point, wall: Wall):
        cell = self._cell(point)
        assert cell
        cell.wall_remove(wall)
        neighbor = self._cell(point.move(wall.to_direction()))
        if neighbor:
            wall = wall.opposite()
            neighbor.wall_remove(wall)

    def _draw_cell(self, xy: Point):
        if self.win:
            cell = self._cell(xy)
            assert cell
            self._draw_cell_direct(cell)

    def _draw_cell_direct(self, cell: Cell):
        if self.win:
            cell.draw(self.win)
            self._animate()

    def _animate(self):
        if not self.win:
            return
        self.win.redraw()
        sleep(self.speed)

    def _solve_r(self, location: Point, goal: Point):
        cell = self._cell(location)
        assert cell

        cell._visited = True

        if location == goal:
            return True

        for direction in [
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST,
        ]:
            wall = Wall.from_direction(direction)
            if cell.wall_check(wall):
                continue
            neighbor = location.move(direction)
            neighbor_cell = self._cell(neighbor)
            if not neighbor_cell or neighbor_cell._visited:
                continue

            if self.win:
                cell.draw_move(self.win, neighbor_cell, undo=False)
                self._animate()
            solved = self._solve_r(neighbor, goal)
            if solved:
                return solved
            elif self.win:
                cell.draw_move(self.win, neighbor_cell, undo=True)
                self._animate()

        return False

    def solve(self, entrance: Point, goal: Point):
        self._unset_visited()
        solved = self._solve_r(entrance, goal)
        if solved:
            print("Solved!")
        else:
            print("Unsolvable!")
