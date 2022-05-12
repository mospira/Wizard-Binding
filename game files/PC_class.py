from helper import *
import math
import os

par_dir = os.path.dirname(os.path.realpath(__file__))


class PC:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = "Down"
        self.color = None
        self.sprSheet_dir = None
        self.hp = 10
        self.spells = ["fireball"]
        self.items = []
        self.ms = 20  # 15
        self.hitbox = [self.x - 15, self.y - 30, self.x + 15, self.y + 30]
        self.curr_spell_index = 0
        self.invinc_count = 0
        self.invinc_state = False
        self.curr_room = None
        self.enemies_slain = 0
        self.spells_cast = 0

    def updateSprSheetDir(self, color):
        if color == "dark":
            self.sprSheet_dir = par_dir + "/sprites/player_sprites/mage-dark.png"
        elif color == "light":
            self.sprSheet_dir = par_dir + "/sprites/player_sprites/mage-light.png"

    def addSpell(self, spell):
        self.spells.append(spell)

    def removeSpell(self, spellName):
        self.spells.remove(spellName)

    def changeMS(self, factor):
        self.ms *= factor

    def updateHitbox(self):
        self.hitbox = [self.x - 15, self.y - 30, self.x + 15, self.y + 30]

    def takeDamage(self, dmg):
        self.hp -= dmg

    def getTeleportPos(self, x, y):
        x1, y1 = self.x, self.y
        x2, y2 = x, y
        x, y = x2 - x1, y1 - y2
        angle = math.atan2(y, x)
        rx = self.x + self.tp_range * math.cos(angle)
        ry = self.y - self.tp_range * math.sin(angle)
        return (rx, ry)

    def getHP_spr_dir(self):
        return par_dir + "/health_bar_pngs/hp{}.png".format(str(self.hp))


def cropPlayerSpriteSheet(dir, image):
    result = []
    width, height = image.size
    lx, ly = width / 3, height / 4
    if dir == "Up":
        for i in range(3):
            result.append(image.crop((lx * i, 0, lx * (i + 1), ly)))
    elif dir == "Right":
        for i in range(3):
            result.append(image.crop((lx * i, ly, lx * (i + 1), ly * 2)))
    elif dir == "Down":
        for i in range(3):
            result.append(image.crop((lx * i, ly * 2, lx * (i + 1), ly * 3)))
    elif dir == "Left":
        for i in range(3):
            result.append(image.crop((lx * i, ly * 3, lx * (i + 1), ly * 4)))
    return result

