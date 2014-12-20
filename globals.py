__author__ = 'JacobWunder'

from kivy.core.audio import SoundLoader
from kivy.core.window import Window

import platform

PLATFORM = platform.system()

BUZZ1 = SoundLoader.load('assets/sounds/buzz1.wav')
BUZZ2 = SoundLoader.load('assets/sounds/buzz2.wav')
BUZZ3 = SoundLoader.load('assets/sounds/buzz3.wav')

GLOBALS = {
    "font": "assets/fonts/Courier New.ttf",
    "font bold": "assets/fonts/Courier New Bold.ttf",
    "line width": 3.0,
    "max velocity": 8,
    "attackercolor": (1.0, 100.0 / 255.0, 100.0 / 255.0),
    "defendercolor": (120.0 / 255.0, 120.0 / 255.0, 1.0),
    "lasercolor": (120.0 / 255.0, 1.0, 120.0 / 255.0),
    "heartchar": u'\u2665',
    "attackeramount": 4,
    "mode": "drag",
    "shooting sound list": [BUZZ1, BUZZ2, BUZZ3],
    "spring": 0.9,
}

if PLATFORM == "Darwin":
    ENTITY = {
        "accl": 0.2,
        "max velocity": 8,
    }

DEFAULTJSON = [["--", "--"], ["--", "--"], ["--", "--"], ["--", "--"], ["--", "--"], ["--", "--"], ["--", "--"], ["--", "--"], ["--", "--"], ["--", "--"]]