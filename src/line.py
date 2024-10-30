import tkinter
from point import Point


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.x1 = p1.x
        self.x2 = p2.x
        self.y1 = p1.y
        self.y2 = p2.y

    def draw(self, canvas: tkinter.Canvas, fill_colour: str):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill=fill_colour, width=2
        )
