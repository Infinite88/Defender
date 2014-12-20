__author__ = 'JacobWunder'
__version__ = 1.0

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Line, Ellipse
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from math import atan2, cos, sin
from math import pi
from random import choice

from globals import GLOBALS
from defender import Defender
from attacker import Attacker
from laser import Laser


class GameScreen(Screen):
    def __init__(self, name="Game"):
        super(GameScreen, self).__init__()
        self.layout = self.ids.layout
        self.name = name
        self.attackers = []
        self.lasers = []
        self.explosions = []
        self.gameInit()
        self.healthBar = self.ids.healthBar
        self.healthBar.text = u'[color=FF7878][font={0}]\u2665'.format(GLOBALS["font"]) * (self.defender.health / 10)
        self.scoreBar = self.ids.scoreBar
        self.scoreBar.text = u"[font={0}]".format(GLOBALS["font"]) + str(self.defender.score)  # [color=78FF78]
        self.defender.master = self
        self.layout.add_widget(self.defender)
        self.soundsBool = False

        self.spring = GLOBALS["spring"]

    def gameInit(self):
        self.defender = Defender(master=self)
        self.spawnEntities()

    def spawnEntities(self):

        for a in range(GLOBALS["attackeramount"]):
            self.attackers.append(Attacker(self.defender))

        for a in self.attackers:
            self.layout.add_widget(a)

    def update(self, latency):
        #print "latency: " + str(latency)
        for entity in [self.defender] + self.attackers + self.lasers:
            entity.update()
            # entity.update()
            # entity.update()
            # entity.update()
            # entity.update()
            # entity.update()
            # entity.update()
            # entity.update()
            # entity.update()
            # entity.update()
            # entity.update()
            entity.draw()
            self.checkCollisions(entity, [self.defender] + self.attackers + self.lasers)
            ####ATTACKERS####
            if isinstance(entity, Attacker):
                if self.defender.x < entity.x:
                    entity.vx -= entity.accl
                elif self.defender.x > entity.x:
                    entity.vx += entity.accl

                if self.defender.y < entity.y:
                    entity.vy -= entity.accl
                elif self.defender.y > entity.y:
                    entity.vy += entity.accl
                    ########
                if entity.alive is False:
                    self.respawn(entity)

            ####DEFENDERS####
            elif isinstance(entity, Defender):
                if entity.health == 0:
                    self.endGame()
            ####LASERS####
            elif isinstance(entity, Laser):
                pass

    def respawn(self, attacker):
        explosion = Explosion(attacker.x, attacker.y)
        self.explosions.append(explosion)
        self.layout.add_widget(explosion)
        Clock.schedule_once(lambda x: self.killExplosion(explosion), 0.5)

        self.attackers.remove(attacker)
        self.layout.remove_widget(attacker)

        new = Attacker(self.defender)
        self.attackers.append(new)
        self.layout.add_widget(new)

    def killExplosion(self, explosion):
        try:
            self.layout.remove_widget(explosion)
            self.explosions.remove(explosion)
        except ValueError:
            print("the game had already ended")

    def checkCollisions(self, entity, entities):
        for other in entities:
            if entity is not other:
                dx = other.x - entity.x
                dy = other.y - entity.y
                minDist = other.radius + entity.radius
                otherxy = Vector(other.x, other.y)
                selfxy = Vector(entity.x, entity.y)
                if selfxy.distance(otherxy) < minDist:
                    angle = atan2(dy, dx)

                    targetX = entity.x + cos(angle) * minDist
                    targetY = entity.y + sin(angle) * minDist

                    ax = (targetX - other.x) * entity.spring
                    ay = (targetY - other.y) * entity.spring

                    self.collide(entity, other, ax, ay)

    def collide(self, entity, other, ax, ay):
        ####ENTITY is ATTACKER####
        if isinstance(entity, Attacker) and (isinstance(other, (Defender, Attacker))):
            entity.vx -= ax
            entity.vy -= ay
        elif isinstance(entity, Attacker) and isinstance(other, Laser):
            self.defender.score += 1
            self.scoreBar.text = \
                "[font={0}]{1}".format(GLOBALS["font"], self.defender.score)
            self.scoreBar.texture_update()
            entity.alive = False
        ####ENTITY is DEFENDER####
        if isinstance(entity, Defender) and isinstance(other, Attacker):
            self.defender.damage()
            # if self.mode == "joystick":
            #     entity.vx -= ax
            #     entity.vy -= ay

    def on_touch_down(self, touch):
        angleList = (0, pi / 2, pi, (3 * pi) / 2)
        if self.defender.loadRadius >= self.defender.loadLimit:
            if self.soundsBool is True:
                choice(GLOBALS["shooting sound list"]).play()

            self.defender.loadRadius = 0
            for laser in self.lasers:
                Clock.unschedule(laser.update)
                laser.canvas.clear()
            del self.lasers[:]
            for i in range(4):
                self.lasers.append(Laser(self.defender.x, self.defender.y, self.defender.radius,
                                         self.defender.laserAngle + angleList[i], self.defender.blasterLength))
            for laser in self.lasers:
                self.layout.add_widget(laser)

    def endGame(self):
        del [self.defender][:]
        del self.attackers[:]
        del self.lasers[:]
        del self.explosions[:]
        self.manager.goto("DEATH")


class Explosion(Image):
    def __init__(self, x, y):
        super(Explosion, self).__init__()
        self.center_x = x
        self.center_y = y
        self.source = "assets/Explosion.zip"
        self.anim_delay = 0.05
        self.size_hint = (0.2, 0.2)

kv = """
<GameScreen>:
    FloatLayout:
        id: layout
        Widget:
            id: ui
            Label:
                id:healthLabel
                text: "[font={0}]health:"
                markup: True
                x: 30
                y: root.height - 25
                size: self.texture_size

            Label:
                id: healthBar
                #text: u'[color=FF7878][font={0}]\u2665' * (root.defender.health / 10)
                font_size: 35
                markup: True
                x: 30
                y: root.height - 60
                size: self.texture_size

            Label:
                id:scoreLabel
                text: "[font={0}]score:"
                markup: True
                x: root.width - self.width - 20
                y: root.height - 25
                size: self.texture_size

            Label:
                id: scoreBar
                #text: u"[font={0}]" + str(root.defender.score)# + "[/font]" #[color=78FF78]
                markup: True
                size: self.texture_size
                x: root.width - self.width - 30
                y: root.height - 60
                font_size: 35
""".format(GLOBALS["font"])
Builder.load_string(kv)