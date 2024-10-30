from cell import Cell, Wall
from line import Line
from point import Point
from window import Window


def gen_cells() -> list[Cell]:
    cells = []
    last_i = 100
    for i in range(200, 701, 100):
        last_j = 100
        for j in range(200, 501, 100):
            c = Cell(Point(last_i, last_j), Point(i, j))
            if not i % 200:
                c.wall_set(Wall.SOUTH_WALL)
            if not j % 200:
                c.wall_set(Wall.EAST_WALL)

            if not i % 300:
                c.wall_set(Wall.NORTH_WALL)
            if not j % 300:
                c.wall_set(Wall.WEST_WALL)
            print(c)
            cells.append(c)
            last_j = j
        last_i = i

    return cells


def main():
    win = Window(800, 600)
    cells = gen_cells()
    for c in cells:
        c.draw(win)

    cells[0].draw_move(win, cells[1])

    win.wait_for_close()


if __name__ == "__main__":
    main()
