__author__ = 'JacobWunder'
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Line, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from math import pi
from random import choice

from globals import GLOBALS
from defender import Defender
from laser import Laser


class HomeScreen(Screen):
    def __init__(self, name="Home"):
        super(HomeScreen, self).__init__()
        self.layout = self.ids.layout
        self.name = name
        self.soundsBool = False
        self.lasers = []
        self.defender = Defender(master=self)
        self.layout.add_widget(self.defender)

        self.gameButton = self.ids.startButton
        self.gameButton.bind(on_release=self.gotoGame)

        self.scoresButton = self.ids.scoresButton
        self.scoresButton.bind(on_release=self.gotoScores)

        Window.bind(on_touch_down=self.shoot)

    def gotoGame(self, *args):
        self.manager.goto("GAME")

    def gotoScores(self, *args):
        self.manager.goto("SCORES")

    def update(self, *args):
        self.defender.update()
        self.defender.draw()
        for laser in self.lasers:
            laser.update()
            laser.draw()

    def shoot(self, *args):
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

kv = """
<HomeScreen>:
    FloatLayout:
        padding: 100
        id: layout
        orientation: 'vertical'
        Widget:
            id: ui
            Image:
                id: iconImage
                source: "assets/icon.png"
                #size_hint: 0.7, 0.7
                #width: root.width / 2.6
                #height: root.height / 8
                center_x: root.width / 2
                center_y: root.height / 2 + 100
                allow_stretch: True
                keep_ratio: False
                size: 400, 400

            Button:
                id:startButton
                text: "[font={0}]Ready for Battle[/font]"
                markup: True
                font_size: 26
                width: root.width / 2.6
                height: root.height / 8
                center_x: root.width / 2
                center_y: root.height / 2 - 100
                size_hint: 0.3846, 0.125


            Button:
                id: scoresButton
                text: "[font={0}]High Scores[/font]"
                markup: True
                font_size: 26
                width: root.width / 2.6
                height: root.height / 8
                center_x: root.width / 2
                center_y: root.height / 2 - 200
                size_hint: 0.3846, 0.125

""".format(GLOBALS["font"])
Builder.load_string(kv)