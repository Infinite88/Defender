__author__ = 'JacobWunder'
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector
from math import cos, sin, sqrt
from math import pi as PI
from random import randint, choice
from kivy.clock import Clock

from globals import GLOBALS
from laser import Laser
from entity import Entity


class Defender(Entity):
    health = 100

    def __init__(self, master=None):
        super(Defender, self).__init__()

        self.SCREENWIDTH = Window.width
        self.SCREENHEIGHT = Window.height

        self.radius = Window.width / 24
        # if self.radius >= 30:
        #     self.radius = 30
        self.blasterLength = self.radius * .5
        self.loadRadius = self.radius / 2  # 15.00
        self.loadLimit = self.radius / 2  # 15.00

        self.master = master
        self.bgColor = GLOBALS["defendercolor"]
        self.laserColor = GLOBALS["lasercolor"]
        self.mode = GLOBALS["mode"]
        self.lineWidth = GLOBALS["line width"]
        self.soundList = GLOBALS["shooting sound list"]

        if self.mode == "drag":
            self.updatePos = self.getMouseXY
        elif self.mode == "joystick":
            self.updatePos = self.updateControlled
            from controller import JoyStickWidget
            self.control = JoyStickWidget(self)
            self.master.add_widget(self.control)

        self.x = Window.width / 2
        self.y = Window.height / 2
        self.laserAngle = 0
        self.lasers = []
        self.damageTime = 0
        self.score = 0
        self.accl = 0.2
        self.acclx = 0
        self.accly = 0
        self.vx = 0
        self.vy = 0
        self.v = 0
        self.friction = 0.6
        self.spring = 0.9
        self.velocityMax = GLOBALS["max velocity"]
        self.addedTo = True

        Window.bind(on_touch_move=self.on_touch_move)

    def updateControlled(self):
        if self.control.inRange():
            dx, dy = self.control.calcTan(
                self.control.im.center_x,
                self.control.im.center_y,
                Window.mouse_pos[0],
                Window.mouse_pos[1]
            )
            self.v = sqrt(dx ** 2 + dy ** 2)
            self.acclx = dx / self.v
            self.accly = dy / self.v

        else:
            if self.acclx > 0:
                self.acclx -= self.accl
            elif self.acclx < 0:
                self.acclx += self.accl
            if self.accly > 0:
                self.accly -= self.accl
            elif self.accly < 0:
                self.accly += self.accl

        self.vx += self.acclx
        self.vy += self.accly

        if self.vx > self.VELOCITYMAX:
            self.vx = self.VELOCITYMAX
        elif self.vx < -1 * self.VELOCITYMAX:
            self.vx = -1 * self.VELOCITYMAX
        if self.vy > self.VELOCITYMAX:
            self.vy = self.VELOCITYMAX
        elif self.vy < -1 * self.VELOCITYMAX:
            self.vy = -1 * self.VELOCITYMAX

        self.x += self.vx
        self.y += self.vy

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

    def getMouseXY(self, *args):
        self.x, self.y = Window.mouse_pos[0], Window.mouse_pos[1]

    def on_touch_move(self, touch, *args):
        try:
            self.x = touch.pos[0]
            self.y = touch.pos[1]
        except AttributeError:
            pass
            # print("'WindowPygame' object has no attribute 'pos'")

    def update(self, *args):
        self.canvas.clear()

        #self.updatePos()

        if self.health > 0:
            if self.laserAngle <= 360.00:
                self.laserAngle += 0.02
            else:
                self.laserAngle = 0.0

            if len(self.lasers) > 0:
                for laser in self.lasers:
                    laser.update()

            if self.loadRadius <= self.loadLimit:
                self.loadRadius += self.loadLimit / 75.0  # 0.2

            if self.damageTime < 50:
                self.damageTime += 1

    def draw(self):
        """Draws lasers"""
        with self.canvas:
            Color(self.bgColor[0], self.bgColor[1], self.bgColor[2])
            Line(circle=(self.x, self.y, self.radius),
                 width=self.lineWidth)
            #Right
            Line(points=[self.x + self.radius * (cos(self.laserAngle)),
                 self.y + self.radius * sin(self.laserAngle),
                 self.x + ((self.radius + self.blasterLength) * cos(self.laserAngle)),
                 self.y + ((self.radius + self.blasterLength) * sin(self.laserAngle))],
                 width=self.lineWidth)
            #Bottom shooter, was degrees((3.0 * PI) / 2.0)
            Line(points=[self.x + self.radius * (cos(self.laserAngle + ((3.0 * PI) / 2.0))),
                 self.y + self.radius * sin(self.laserAngle + ((3.0 * PI) / 2.0)),
                 self.x + ((self.radius + self.blasterLength) * cos(self.laserAngle + ((3.0 * PI) / 2.0))),
                 self.y + ((self.radius + self.blasterLength) * sin(self.laserAngle + ((3.0 * PI) / 2.0)))],
                 width=self.lineWidth)
            #Left shooter, was degrees(PI)
            Line(points=[self.x + self.radius * (cos(self.laserAngle + (PI))),
                 self.y + self.radius * sin(self.laserAngle + (PI)),
                 self.x + ((self.radius + self.blasterLength) * cos(self.laserAngle + (PI))),
                 self.y + ((self.radius + self.blasterLength) * sin(self.laserAngle + (PI)))],
                 width=self.lineWidth)
            #Top shooter, was degrees(PI / 2)
            Line(points=[self.x + self.radius * cos(self.laserAngle + (PI / 2)),
                 self.y + self.radius * sin(self.laserAngle + (PI / 2)),
                 self.x + ((self.radius + self.blasterLength) * cos(self.laserAngle + (PI / 2))),
                 self.y + ((self.radius + self.blasterLength) * sin(self.laserAngle + (PI / 2)))],
                 width=self.lineWidth)

            Color(self.laserColor[0], self.laserColor[1], self.laserColor[2])
            Line(circle=(self.x, self.y, self.loadRadius),
                 width=self.lineWidth)

    def on_touch_down(self, *args):
        if self.loadRadius >= self.loadLimit:
            choice(self.soundList).play()
            self.loadRadius = 0

    def damage(self):
        if self.damageTime == 50:
            self.health -= 10
            self.loadRadius = 0.0
            self.damageTime = 0
            self.master.healthBar.text = \
                '[color=FF7878][font={0}]'.format(GLOBALS["font"]) + u'\u2665' * (self.health / 10)
            self.master.healthBar.texture_update()

