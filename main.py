__author__ = 'JacobWunder'
import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import json

from homescreen import HomeScreen
from deathscreen import DeathScreen
from gamescreen import GameScreen
from scoresscreen import ScoresScreen
from globals import GLOBALS, DEFAULTJSON
from space import Space


class DefenderRoot(ScreenManager):
    def __init__(self):
        super(DefenderRoot, self).__init__()
        self.homeScreen = HomeScreen(name="Home")
        self.gameScreen = GameScreen(name="Game")
        self.deathScreen = DeathScreen(name="Death")
        self.scoresScreen = ScoresScreen(name="Scores")

        self.checkScoresFile()

        self.add_widget(self.homeScreen)
        Clock.schedule_interval(self.current_screen.update, 1.0 / 60.0)

    def checkScoresFile(self):
        try:
            open("assets/scores.json", "r")
        except IOError:
            with open("assets/scores.json", "w+") as scores:
                obj = DEFAULTJSON
                scores.write(json.dumps(obj))

    def goto(self, new):
        Clock.unschedule(self.current_screen.update)

        print(("Going to the %s" % new) + " screen")
        if new == "HOME":
            self.switch_to(self.homeScreen, direction="right")

        elif new == "GAME":
            del self.gameScreen
            self.gameScreen = GameScreen(name="Game")
            self.switch_to(self.gameScreen, direction="left")

        elif new == "DEATH":
            self.deathScreen.score = self.gameScreen.defender.score
            self.deathScreen.init()
            self.switch_to(self.deathScreen, transition=NoTransition(), direction="left")

        elif new == "SCORES":
            self.scoresScreen.scoreInit()
            self.switch_to(self.scoresScreen, direction="left")

        Clock.schedule_interval(self.current_screen.update, 1.0 / 60.0)


class DefenderApp(App):
    icon = "assets/icon.png"
    title = "Defender"

    def build(self):
        root = DefenderRoot()
        space = Space()
        Window.add_widget(space)
        return root

if __name__ == "__main__":
    DefenderApp().run()

