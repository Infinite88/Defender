__author__ = "JacobWunder"
from math import cos, sin, tan
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle, Bezier
from kivy.clock import Clock
from kivy.core.window import Window
from globals import GLOBALS
from entity import Entity


class Laser(Entity):
    def __init__(self, defx, defy, defr, angle, length):
        super(Laser, self).__init__()
        self.angle = angle
        self.color = GLOBALS["lasercolor"]

        self.x0 = defx + defr * cos(angle)
        self.y0 = defy + defr * sin(angle)
        self.x1 = defx + (defr + length) * cos(angle)
        self.y1 = defy + (defr + length) * sin(angle)

    def update(self, *args):
        self.pos = (self.x0, self.y0)
        self.canvas.clear()

        ####CHANGED FROM 10 ORIGINALLY TEN###
        self.x0 += 10 * cos(self.angle)
        self.y0 += 10 * sin(self.angle)
        self.x1 += 10 * cos(self.angle)
        self.y1 += 10 * sin(self.angle)

    def draw(self):
        with self.canvas:
            Color(self.color[0], self.color[1], self.color[2])
            Line(points=[self.x0, self.y0,
                         self.x1, self.y1],
                 width=GLOBALS["line width"])
