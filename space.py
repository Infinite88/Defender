from kivy.uix.widget import Widget
from kivy.graphics import Line, Color
from kivy.core.window import Window

from random import randint


class Space(Widget):
    def __init__(self):
        super(Space, self).__init__()
        self.sizeVariation = 3
        self.spaceBetween = 20
        self.starList = []
        self.starAmount = 100
        self.height = Window.height
        self.width = Window.width
        self.x = 0
        self.y = 0
        self.getRandomPoints()
        self.update()

        Window.bind(on_resize=self.resize)
        
    def getRandomPoints(self):
        for star in range(self.starAmount):
            pos = (randint(0, self.width), randint(0, self.height))
            self.starList.append(pos)

    def update(self):
        with self.canvas.before:
            Color(1, 1, 1)
            for pos in self.starList:
                Line(circle=(pos[0], pos[1], randint(1, self.sizeVariation)))

    def resize(self, *args):
        self.height = Window.height
        self.width = Window.width
        self.starList = []
        self.getRandomPoints()
        self.update()
