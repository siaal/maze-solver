#!/bin/python3
from cell import Cell, Wall
from maze import Maze
from point import Point
from window import Window


def main():
    win_width = 1000
    win_height = 800
    win = Window(win_width, win_height)
    offset_x = 100
    offset_y = 100
    cols = 25
    rows = 25
    width = (win_width - offset_x) // cols
    height = (win_height - offset_y) // rows
    m = Maze(
        win,
        Point(offset_x, offset_y),
        n_rows=rows,
        n_cols=cols,
        cell_width=width,
        cell_height=height,
        speed=0.001,
    )
    start = lambda _: start_maze(m)
    win.bind("<space>", start)
    win.wait_for_close()


def start_maze(m: Maze):
    m.draw_cells()
    m.speed = 0.005
    m.break_entrance_and_exit()
    m._break_walls(m.exit_point)
    m.speed = 0.05
    m.solve(m.entrance_point, m.exit_point)


if __name__ == "__main__":
    main()
