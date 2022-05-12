from helper import *
import math

par_dir = os.path.dirname(os.path.realpath(__file__))
"""
This file formally defines the Spell class.

"""

class Spell:
    def __init__(self, name, x, y, sprSheet_dir, coords):
        self.sprSheet_dir = sprSheet_dir
        self.castpos_x, self.castpos_y = x, y
        self.x, self.y = coords[0], coords[1]
        self.dest_x, self.dest_y = coords[2], coords[3]
        self.ms = 15
        self.dmg = 5
        self.image = None

    def getOrientation(self):
        x1, y1 = self.castpos_x, self.castpos_y
        x2, y2 = self.dest_x, self.dest_y
        x, y = x2 - x1, y1 - y2
        angle = math.degrees(math.atan2(y, x))
        return angle

    def getCoords(self):
        return (self.x, self.y)

    def changeMS(self, factor):
        self.ms *= factor

    def inHitbox(self, x,y):
        return math.dist((self.x, self.y), (x,y)) < 30
        return hitbox[0] <= self.x <= hitbox[2] and hitbox[1] <= self.y <= hitbox[3]


def getDirectory(spell):  # go here to add more spells
    if spell == "fireball":
        return par_dir + "/sprites/fireball.png"
