from tkinter import Tk, BOTH, Canvas

from line import Line


class Window:
    def __init__(self, width, height, title=""):
        self._root = Tk()
        self._root.title(title)
        self._root.protocol("WM_DELETE_WINDOW", self.close)

        self._canvas = Canvas(height=height, width=width)
        self._canvas.pack()

        self._running = False

    def redraw(self):
        self._root.update_idletasks()  # TODO: Redundant?
        self._root.update()

    def wait_for_close(self):
        self._running = True
        while self._running:
            self.redraw()
        print("Closing gracefully")

    def close(self):
        self._running = False
        print("close cmd sent")

    def draw_line(self, line: Line, fill_colour: str):
        line.draw(self._canvas, fill_colour)

    def bind(self, binding, f):
        print("ACTIVATING")
        self._root.bind(binding, f)
