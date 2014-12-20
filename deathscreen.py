__author__ = 'JacobWunder'
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Line, Ellipse
from kivy.core.window import Window
from kivy.lang import Builder
import json

from globals import GLOBALS


class DeathScreen(Screen):
    def __init__(self, name="Death"):
        super(DeathScreen, self).__init__()
        self.name = name
        self.score = 0
        self.textInput = self.ids.textInput
        self.homeButton = self.ids.homeButton
        self.respawnButton = self.ids.respawnButton
        self.scoreLabel = self.ids.scoreLabel

        Window.bind(on_key_down=self.keyboardListener)
        self.homeButton.bind(on_release=lambda x: self.goto("HOME"))
        self.respawnButton.bind(on_release=lambda x: self.goto("GAME"))
        self.init()

    def init(self):
        self.scoreLabel.text = "[color=000000]Score: " + str(self.score)
        self.scoreLabel.texture_update()

    def update(self, *args):
        self.textInput.text = self.textInput.text[:3]
        #print(self.score)

    def keyboardListener(self, *args):
        if args[2] == 36:
            self.manager.goto("HOME")

    def logScores(self):
        scores = open("assets/scores.json", "r+")
        data = json.load(scores)
        print(data)
        for score in range(len(data)):
            print(data[score][0], data[score][1])
            if data[score][1] != '--' and self.score > int(data[score][1]):
                data.insert(score, [self.textInput.text, self.score])
                print("LAST DATA", data[-1])
                data.pop(len(data) - 1)
                break

            elif data[score][1] == '--':
                data[score][0] = self.textInput.text
                data[score][1] = self.score
                break
        scores.close()
        data = json.dumps(data, sort_keys=True)
        scores = open("assets/scores.json", "w")
        scores.write(data)

    def goto(self, new):
        self.logScores()
        self.manager.goto(new=new)

kv = """
<DeathScreen>:
    FloatLayout:
        id: layout
        Widget:
            id: ui
            Image:
                id: explosionImage
                source: "assets/explosion1.png"
                allow_stretch: True
                keep_ratio: False
                center_x: root.center_x
                center_y: root.center_y + 50
                size: 500, 500

            Label:
                text: "[font={2}]UR FOKING DED M8"
                markup: True
                size: self.texture_size
                center_x: ui.center_x
                center_y: ui.center_y + 50
                font_size: 72

            TextInput:
                id: textInput
                center_x: root.center_x
                center_y: root.center_y - 50
                width: 100
                height: 60
                font_name: "{2}"
                font_size: 36
                background_color: 0.1, 0.1, 0.1, 0.9
                color: {1}
                focus: True
                foreground_color: 1, 1, 1, 1
                #size: self.texture_size

            Label:
                id: initialsLabel
                text: "[font={2}]Initials:"
                markup: True
                font_size: 15
                x: textInput.x
                y: textInput.y + 20

            Label:
                id: scoreLabel
                font_name: "{0}"
                center_x: root.center_x
                center_y: root.center_y + 100
                font_size: 40
                markup: True

            Button:
                id: homeButton
                markup: True
                text: "[font={0}]Start Screen"
                center_x: root.center_x
                center_y: root.center_y - 150
                size: 300, 75
                font_size: 30

            Button:
                id: respawnButton
                markup: True
                text: "[font={0}]Back to Battle"
                center_x: ui.center_x
                center_y: ui.center_y - 250
                size: 300, 75
                font_size: 30


""".format(GLOBALS["font"], GLOBALS["defendercolor"], GLOBALS["font bold"])
Builder.load_string(kv)