from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.graphics import Color, Line, Rectangle
from math import cos, sin, atan2
from random import randint
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

from random import choice
from globals import GLOBALS
from entity import Entity

HEADERHEIGHT = Window.height - 60

class Attacker(Entity):
    """ATTACKER CLASS"""
    def __init__(self, defender, master=None):
        super(Attacker, self).__init__()
        self.defender = defender
        self.SCREENWIDTH = Window.width
        self.SCREENHEIGHT = Window.height
        self.x = randint(0, self.SCREENWIDTH)
        self.y = HEADERHEIGHT + 30
        self.color = GLOBALS["attackercolor"]
        self.velocityMax = GLOBALS["max velocity"]
        self.lineWidth = GLOBALS["line width"]
        self.master = master
        Window.bind(on_resize=self.resize)
        self.radius = Window.width / 30
        # if self.radius >= 25:
        #     self.radius = 15

        self.vx = 0.5
        self.vy = 0.5
        self.accl = 0.2
        self.spring = 0.9
        self.friction = 0.6
        self.alive = True

    def update(self, *args):
        self.canvas.clear()
        self.x += self.vx
        self.y += self.vy

        if self.vx >= self.velocityMax:
            self.vx = self.velocityMax
        if self.vy >= self.velocityMax:
            self.vy = self.velocityMax

        self.collide()

    def draw(self):
        with self.canvas:
            Color(self.color[0], self.color[1], self.color[2])
            Line(points=[self.x, self.y - self.radius,
                 self.x - self.radius, self.y + self.radius,
                 self.x + self.radius, self.y + self.radius],
                 width=self.lineWidth,
                 close=True)

    def collide(self):
        if self.x + self.radius > self.SCREENWIDTH:
            self.x = self.SCREENWIDTH - self.radius
            self.vx *= self.friction
        elif self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= self.friction
            
        if self.y + self.radius > self.SCREENHEIGHT:
            self.y = self.SCREENHEIGHT - self.radius
            self.vy *= self.friction
        elif self.y - self.radius < 0:
            self.y = self.radius
            self.vy *= self.friction

    def resize(self, *args):
        self.SCREENWIDTH = Window.width
        self.SCREENHEIGHT = Window.height
