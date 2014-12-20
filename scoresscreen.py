__author__ = 'JacobWunder'
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Line, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
import json

from globals import GLOBALS


class ScoresScreen(Screen):
    def __init__(self, name="Scores"):
        super(ScoresScreen, self).__init__()
        self.name = name
        self.labels = []
        self.boxLayout = self.ids.boxLayout
        self.floatLayout = self.ids.floatLayout
        self.homeButton = self.ids.homeButton
        self.homeButton.bind(on_release=self.gotoHome)

    def scoreInit(self):
        scoresFile = open("assets/scores.json")
        scores = json.load(scoresFile)
        for i in range(10):
            self.labels.append(self.ids["score%s" % i])

        for i in range(len(self.labels)):
            self.labels[i].text = str(scores[i][0]) + "  -  " + str(scores[i][1])

    def update(self, *args):
        pass

    def gotoHome(self, *args):
        del self.labels[:]
        self.manager.goto("HOME")




kv = """
<ScoresScreen>:
    BoxLayout:
        id: boxLayout
        orientation: "vertical"
        padding: 20,20,20,20
        Label:
            id: score0
            markup: True
            font_name: "{0}"
            font_size: {1}
            #center_x: root.center_x
        Label:
            id: score1
            markup: True
            font_name: "{0}"
            font_size: {1}
            #center_x: root.center_x
        Label:
            id: score2
            markup: True
            font_name: "{0}"
            font_size: {1}
            #center_x: root.center_x
        Label:
            id: score3
            markup: True
            font_name: "{0}"
            font_size: {1}
            #center_x: root.center_x
        Label:
            id: score4
            markup: True
            font_name: "{0}"
            font_size: {1}
            #center_x: root.center_x
        Label:
            id: score5
            markup: True
            font_name: "{0}"
            font_size: {1}
            #center_x: root.center_x
        Label:
            id: score6
            markup: True
            font_name: "{0}"
            font_size: {1}
            #center_x: root.center_x
        Label:
            id: score7
            markup: True
            font_name: "{0}"
            font_size: {1}
            #center_x: root.center_x
        Label:
            id: score8
            markup: True
            font_name: "{0}"
            font_size: {1}
            #center_x: root.center_x
        Label:
            id: score9
            markup: True
            font_name: "{0}"
            font_size: {1}
            #center_x: root.center_x

        Button:
            id: homeButton
            text: "Home Screen"
            width: 300
            font_name: "{0}"
            font_size: {1} - 15

    FloatLayout:
        id: floatLayout
""".format(GLOBALS["font"], str(40))
Builder.load_string(kv)