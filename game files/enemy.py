from helper import *
from floor import *
import math

par_dir = os.path.dirname(os.path.realpath(__file__))
"""
This file formally defines the enemy class
as well as functions by which enemies operate.

"""


class Enemy:
    def __init__(self, x, y, gx, gy, level):
        self.x, self.y = x, y
        self.curr_room = []
        self.hp = level * 2
        self.ms = 10
        self.hitbox = [self.x - 17, self.y - 35, self.x + 17, self.y + 35]
        self.sprite_count = 0
        self.direction = "Down"
        self.homestage = (gx, gy)
        self.path = None

    def updateDirection(self, x, y):
        x_distance, y_distance = abs(self.x - x), abs(self.y - y)
        if x_distance >= y_distance:
            if self.x > x:
                self.direction = "Left"
                self.x -= self.ms
                self.hitbox[0] -= self.ms
                self.hitbox[2] -= self.ms
            else:
                self.direction = "Right"
                self.x += self.ms
                self.hitbox[0] += self.ms
                self.hitbox[2] += self.ms
        else:
            if self.y > y:
                self.direction = "Up"
                self.y -= self.ms
                self.hitbox[1] -= self.ms
                self.hitbox[3] -= self.ms
            else:
                self.direction = "Down"
                self.y += self.ms
                self.hitbox[1] += self.ms
                self.hitbox[3] += self.ms

    def takeDamage(self, dmg):
        self.hp -= dmg

    def getPath(self, g, start, target):
        return conductPathfind(g, start, target)

    def updateHitbox(self):
        self.hitbox = [self.x - 15, self.y - 30, self.x + 15, self.y + 30]


def getEnemySpritesheetDir():
    return par_dir + "/sprites/enemy_sprites/skeleton_sprites.png"


def cropEnemySpriteSheet(dir, image):
    result = []
    width, height = image.size
    lx, ly = width / 3, height / 4  # down left right up
    if dir == "Down":
        for i in range(3):
            result.append(image.crop((lx * i, 0, lx * (i + 1), ly)))
    elif dir == "Left":
        for i in range(3):
            result.append(image.crop((lx * i, ly, lx * (i + 1), ly * 2)))
    elif dir == "Right":
        for i in range(3):
            result.append(image.crop((lx * i, ly * 2, lx * (i + 1), ly * 3)))
    elif dir == "Up":
        for i in range(3):
            result.append(image.crop((lx * i, ly * 3, lx * (i + 1), ly * 4)))
    return result


def createGraph(grid):
    result = dict()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 0:
                result[(i, j)] = []
                adjacents = getAdjacents(grid, i, j)
                if adjacents[0] == True:
                    result[(i, j)] += [(i - 1, j)]
                if adjacents[1] == True:
                    result[(i, j)] += [(i + 1, j)]
                if adjacents[2] == True:
                    result[(i, j)] += [(i, j - 1)]
                if adjacents[3] == True:
                    result[(i, j)] += [(i, j + 1)]
            continue
    return result


def conductPathfind(g, start, target):  # Modified code from Kelly Rivers, CMU 15110 Search Algorithms II Powerpoint
    """
    It takes a graph, a starting node, and a target node, and returns a list of nodes that are visited
    in order to get from the starting node to the target node
    
    :param g: The graph to be searched
    :param start: The starting node
    :param target: The node you want to get to
    :return: The path from the start to the target.
    """
# A breadth first search algorithm.
    g = createGraph(g)
    visited = []
    nextNodes = [start]
    while len(nextNodes) > 0:
        nextNode = nextNodes[0]
        if nextNode == target:
            return visited + [target]
        else:
            for node in g[nextNode]:
                if node in nextNodes:
                    nextNodes.remove(node)
                if node not in visited and node not in nextNodes:
                    nextNodes = [node] + nextNodes
        nextNodes.remove(nextNode)
        visited.append(nextNode)
    return visited


def getPathfindChance(time):
    return random.random() > 0.70 and time % 3 == 0
