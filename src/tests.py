import unittest

from cell import Cell, Wall
from maze import Maze
from point import Point


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        cols = 12
        rows = 16
        top_left = Point(0, 0)
        m1 = Maze(None, top_left, rows, cols, 10, 10)
        self.assertEqual(len(m1._cells), rows)  # [row][column] access
        for row in m1._cells:
            self.assertEqual(len(row), cols)

        cols = 5
        rows = 5
        top_left = Point(0, 0)
        m1 = Maze(None, top_left, rows, cols, 10, 10)

        cells = m1._cells
        zero = cells[0][0]
        self.assertListEqual(
            [zero._top, zero._left, zero._bot, zero._right], [40, 0, 50, 10]
        )
        one = cells[0][1]
        self.assertListEqual(
            [one._top, one._left, one._bot, one._right], [40, 10, 50, 20]
        )
        two = cells[0][2]
        self.assertListEqual(
            [two._top, two._left, two._bot, two._right], [40, 20, 50, 30]
        )
        one_zero = cells[1][0]
        self.assertListEqual(
            [one_zero._top, one_zero._left, one_zero._bot, one_zero._right],
            [30, 00, 40, 10],
        )
        one_one = cells[1][1]
        self.assertListEqual(
            [one_one._top, one_one._left, one_one._bot, one_one._right],
            [30, 10, 40, 20],
        )
        four_zero = cells[4][0]
        self.assertListEqual(
            [four_zero._top, four_zero._left, four_zero._bot, four_zero._right],
            [00, 0, 10, 10],
        )
        four_one = cells[4][1]
        self.assertListEqual(
            [four_one._top, four_one._left, four_one._bot, four_one._right],
            [0, 10, 10, 20],
        )
        four_four = cells[4][4]
        self.assertListEqual(
            [four_four._top, four_four._left, four_four._bot, four_four._right],
            [0, 40, 10, 50],
        )

    def test_opposites(self):
        north = Wall.NORTH_WALL
        south = Wall.SOUTH_WALL
        east = Wall.EAST_WALL
        west = Wall.WEST_WALL
        self.assertEqual(north.opposite(), south)
        self.assertEqual(east.opposite(), west)
        self.assertEqual(south.opposite(), north)
        self.assertEqual(west.opposite(), east)

    def test_maze_remove_wall(self):
        make_maze = lambda: Maze(None, Point(0, 0), 10, 10, 10, 10)
        m1 = make_maze()
        for row in m1._cells:
            for cell in row:
                self.assertTrue(cell.wall_check(Wall.NORTH_WALL))
                self.assertTrue(cell.wall_check(Wall.EAST_WALL))
                self.assertTrue(cell.wall_check(Wall.SOUTH_WALL))
                self.assertTrue(cell.wall_check(Wall.WEST_WALL))

        m1 = make_maze()
        self.assertTrue(m1._cells[5][5].wall_check(Wall.EAST_WALL))
        self.assertTrue(m1._cells[6][5].wall_check(Wall.WEST_WALL))
        m1.remove_wall(Point(5, 5), Wall.EAST_WALL)
        self.assertFalse(m1._cells[5][5].wall_check(Wall.EAST_WALL))
        self.assertFalse(m1._cells[6][5].wall_check(Wall.WEST_WALL))

        m1 = make_maze()
        self.assertTrue(m1._cells[5][5].wall_check(Wall.SOUTH_WALL))
        self.assertTrue(m1._cells[5][4].wall_check(Wall.NORTH_WALL))
        m1.remove_wall(Point(5, 5), Wall.SOUTH_WALL)
        self.assertFalse(m1._cells[5][5].wall_check(Wall.SOUTH_WALL))
        self.assertFalse(m1._cells[5][4].wall_check(Wall.NORTH_WALL))

        m1 = make_maze()
        self.assertTrue(m1._cells[5][5].wall_check(Wall.WEST_WALL))
        self.assertTrue(m1._cells[4][5].wall_check(Wall.EAST_WALL))
        m1.remove_wall(Point(5, 5), Wall.WEST_WALL)
        self.assertFalse(m1._cells[5][5].wall_check(Wall.WEST_WALL))
        self.assertFalse(m1._cells[4][5].wall_check(Wall.EAST_WALL))

        m1 = make_maze()
        self.assertTrue(m1._cells[5][5].wall_check(Wall.NORTH_WALL))
        self.assertTrue(m1._cells[5][6].wall_check(Wall.SOUTH_WALL))
        m1.remove_wall(Point(5, 5), Wall.NORTH_WALL)
        self.assertFalse(m1._cells[5][5].wall_check(Wall.NORTH_WALL))
        self.assertFalse(m1._cells[5][6].wall_check(Wall.SOUTH_WALL))

    def test_cell_wall_remove(self):
        make_cell = lambda: Cell(Point(0, 0), Point(10, 10))

        c = make_cell()
        self.assertTrue(c.wall_check(Wall.NORTH_WALL))
        self.assertTrue(c.wall_check(Wall.EAST_WALL))
        self.assertTrue(c.wall_check(Wall.SOUTH_WALL))
        self.assertTrue(c.wall_check(Wall.WEST_WALL))

        c = make_cell()
        c.wall_remove(Wall.NORTH_WALL)
        self.assertFalse(c.wall_check(Wall.NORTH_WALL))
        self.assertTrue(c.wall_check(Wall.EAST_WALL))
        self.assertTrue(c.wall_check(Wall.SOUTH_WALL))
        self.assertTrue(c.wall_check(Wall.WEST_WALL))
        c.wall_remove(Wall.NORTH_WALL)
        self.assertFalse(c.wall_check(Wall.NORTH_WALL))
        self.assertTrue(c.wall_check(Wall.EAST_WALL))
        self.assertTrue(c.wall_check(Wall.SOUTH_WALL))
        self.assertTrue(c.wall_check(Wall.WEST_WALL))

        c = make_cell()
        c.wall_remove(Wall.WEST_WALL)
        self.assertTrue(c.wall_check(Wall.NORTH_WALL))
        self.assertTrue(c.wall_check(Wall.EAST_WALL))
        self.assertTrue(c.wall_check(Wall.SOUTH_WALL))
        self.assertFalse(c.wall_check(Wall.WEST_WALL))

        c = make_cell()
        c.wall_remove(Wall.SOUTH_WALL)
        self.assertTrue(c.wall_check(Wall.NORTH_WALL))
        self.assertTrue(c.wall_check(Wall.EAST_WALL))
        self.assertFalse(c.wall_check(Wall.SOUTH_WALL))
        self.assertTrue(c.wall_check(Wall.WEST_WALL))

        c = make_cell()
        c.wall_remove(Wall.EAST_WALL)
        self.assertTrue(c.wall_check(Wall.NORTH_WALL))
        self.assertFalse(c.wall_check(Wall.EAST_WALL))
        self.assertTrue(c.wall_check(Wall.SOUTH_WALL))
        self.assertTrue(c.wall_check(Wall.WEST_WALL))


if __name__ == "__main__":
    unittest.main()
