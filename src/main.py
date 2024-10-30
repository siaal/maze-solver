#!/bin/python3
from cell import Cell, Wall
from maze import Maze
from point import Point
from window import Window


def main():
    win = Window(800, 600)
    m = Maze(win, Point(00, 00), 2, 2, 50, 50, speed=0.01)
    m.draw_cells()
    m.break_entrance_and_exit()
    m._break_walls(Point(0, -1))
    win.wait_for_close()


if __name__ == "__main__":
    main()
