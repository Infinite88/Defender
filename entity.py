__author__ = 'JacobWunder'
from kivy.uix.widget import Widget

from globals import GLOBALS


class Entity(Widget):
    def __init__(self):
        super(Entity, self).__init__()
        self.radius = 10
        self.vx = 0
        self.vy = 0
        self.acclx = 0
        self.accly = 0
        self.friction = 0.6
        self.spring = GLOBALS["spring"]
        self.alive = True

    def bottomLeft(self):
        return self.x, self.y

    def topLeft(self):
        return self.x, self.y + self.height

    def bottomRight(self):
        return self.x + self.width, self.y

    def topRight(self):
        return self.x + self.width, self.y + self.height

    def update(self):
        pass