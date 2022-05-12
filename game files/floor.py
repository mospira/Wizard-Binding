from helper import *
import random
import math
import os

par_dir = os.path.dirname(os.path.realpath(__file__))
"""
This file formally defines each floor as a class,
and each stage within said floor as objects of the Stage class,
with corresponding functions.

"""

class Floor:
    def __init__(self, level):
        self.num_rooms = int(random.randint(1, 3) + 5 + 3 * math.log10(level) * 2.6)
        self.curr_room = [3, 3]
        self.floor_cleared = False
        self.pathfinders = []

    def generateFloor(self, rows, cols):
        """
        It takes a grid, a set of visited cells, the current row and column, the number of rows and columns,
        and the number of rooms to generate. It then generates a maze by randomly selecting a direction to
        move in, and if the cell in that direction is not visited, it moves there and adds it to the set of
        visited cells. It then recursively calls itself with the new row and column
        
        :param rows: number of rows in the grid
        :param cols: number of columns
        :return: A list of lists.
        """
        grid = createGrid(8, 8)
        midRow, midCol = int((rows / 2) - 1), int((cols / 2) - 1)
        result = generateMaze(
            grid, {(midRow, midCol)}, midRow, midCol, rows, cols, self.num_rooms
        )
        return result

    def getAllStages(self, floorplan):
        result = []
        for i in range(len(floorplan)):
            for j in range(len(floorplan[0])):
                if floorplan[i][j] != 0:
                    result.append(floorplan[i][j])
        return result

    def getTotalEnemies(self, floorplan):
        result = 0
        lst = self.getAllStages(floorplan)
        for stage in lst:
            result += stage.num_enemies
        return result


class Stage:
    def __init__(self, level, grid, gx, gy):
        self.num_enemies = getNumEnemies(level)
        self.gridPos = (gx, gy)
        self.base_dir = getStageTypeDir()
        self.base_img = None
        self.doors_img = None
        self.walls_imgs = []
        self.deco_imgs = []
        self.doorTypeDir = getDoorTypeDir(grid, gx, gy)
        self.deco_dirs = pickStageDecorations()
        self.walls_dirs = getWallDirs()
        self.enemies = []
        self.stairs_x = None
        self.stairs_y = None
        self.stairs_img = None
        self.stairs_dir = getRandomStairDir()

    def __repr__(self):
        return str(self.gridPos)

    def updateEnemies(self, num):
        self.num_enemies += num

    def inDescendRange(self, x, y):  # 25 px wide 30 pix tall
        max_dist = math.hypot(40, 60)
        dist = math.dist((x, y), (self.stairs_x, self.stairs_y))
        return dist < max_dist


def getRandomStairDir():
    num = random.randint(1, 2)
    dir = par_dir + "/stages/stairs/{}.png".format(num)
    return dir


def getStairsCoords(width, height):
    possible_x = [width / 2 - 64, width / 2 + 64]
    possible_y = [height / 2 - 64, height / 2 + 64]
    x = possible_x[random.randint(0, 1)]
    y = possible_y[random.randint(0, 1)]
    return x, y


def getWallDirs():
    result = []
    for wall in ["top", "bot", "left", "right"]:
        result.append(
            par_dir + "/stages/walls/{}/{}.png".format(wall, 1)
        ) 
    return result


def pickStageDecorations():
    result = []
    roll, max_rolls = 0, 3
    while roll < max_rolls:
        if random.random() < 0.40:
            result.append(par_dir + "/stage_deco/{}.png".format(random.randint(1, 7)))
        roll += 1
    return result


def getNumEnemies(level):
    result = 0
    for i in range(level + 1):
        if random.random() < 0.85:
            result += 1
    return result


def createGrid(rows, cols):
    result = []
    for row in range(rows):
        lst = []
        for i in range(cols):
            lst.append(0)
        result.append(lst)
    return result


def changeCell(dir, row, col):
    if dir == "up":
        row -= 1
    if dir == "down":
        row += 1
    if dir == "left":
        col -= 1
    if dir == "right":
        col += 1
    return (row, col)


def isSolution(grid, visited, max):
    if grid == None:
        return False
    if len(visited) != max:
        return False
    return True


def isLegal(rows, cols, row, col, rooms):
    if row < 0 or row >= rows:
        return False
    if col < 0 or col >= cols:
        return False
    if (row, col) in rooms:
        return False
    if random.random() < 0.5:
        return False
    return True


def generateMazeHelper(grid, rooms, row, col, rows, cols, max):  # maybe use sets here?
    """
    If the current cell is a solution, return the grid. Otherwise, try to move in each direction, and if
    the new cell is legal, add it to the set of rooms, and recursively call the function on the new
    cell. If the new cell is a solution, return the grid. If the new cell is not a solution, remove it
    from the set of rooms, and set the current cell to 0.
    
    :param grid: the grid that we're working with
    :param rooms: a set of tuples of the form (row, col)
    :param row: the row of the current cell
    :param col: the column of the current cell
        :param rows: number of rows in the maze
        :param cols: number of columns in the grid
        :param max: the number of rooms in the maze
    :return: A 2D array of 0s and 1s.
    """
# A recursive function that generates a maze.
    grid[row][col] = 1
    if isSolution(grid, rooms, max):
        return grid
    else:
        for dir in ["up", "down", "left", "right"]:
            new_r, new_c = changeCell(dir, row, col)
            if isLegal(rows, cols, new_r, new_c, rooms):
                rooms.add((new_r, new_c))
                grid = generateMazeHelper(grid, rooms, new_r, new_c, rows, cols, max)
                if isSolution(grid, rooms, max):
                    return grid
        grid[row][col] = 0
        rooms.remove((row, col))
        return grid


def countRooms(grid):
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 0:
                count += 1
    return count


def generateMaze(grid, rooms, row, col, rows, cols, max):
    """
    It tries to generate a maze, and if it fails, it tries again
    
    :param grid: the grid that the maze is being generated on
    :param rooms: a list of all the rooms in the maze
    :param row: the row of the current room
    :param col: the column of the current room
    :param rows: number of rows in the grid
    :param cols: number of columns in the grid
    :param max: the maximum number of rooms to generate
    :return: A grid with a maze.
    """
    while countRooms(grid) < max:
        try:
            grid = generateMazeHelper(grid, rooms, row, col, rows, cols, max)
        except:
            continue
    return grid


def getAdjacents(grid, row, col):
    """
    If the cell is not on the edge of the grid, check if the adjacent cells are not zero.
    
    :param grid: the grid
    :param row: the row of the current cell
    :param col: the column of the current cell
    :return: A list of 4 booleans.
    """
    result = [None, None, None, None]
    rows, cols = len(grid), len(grid[0])
    if 0 < row < rows - 1:
        if grid[row - 1][col] != 0:  # up
            result[0] = True
        if grid[row + 1][col] != 0:  # down
            result[1] = True
    else:
        if row == 0:
            if grid[row + 1][col] != 0:  # down
                result[1] = True
        if row == rows - 1:
            if grid[row - 1][col] != 0:  # up
                result[0] = True
    if 0 < col < cols - 1:
        if grid[row][col - 1] != 0:  # left
            result[2] = True
        if grid[row][col + 1] != 0:  # right
            result[3] = True
    else:
        if col == 0:
            if grid[row][col + 1] != 0:  # right
                result[3] = True
        if col == cols - 1:
            if grid[row][col - 1] != 0:  # left
                result[2] = True
    return result


def getStageTypeDir():
    return par_dir + "/stages/base{}.png".format(random.randint(1, 6))


def getDoorTypeDir(grid, row, col):
    adjacents = getAdjacents(grid, row, col)
    id = ""
    for elmnt in adjacents:
        if elmnt == None:
            id += "0"
        else:
            id += "1"
    dir = par_dir + "/stages/doors/{}.png".format(id)
    return dir


def getID(grid, row, col):
    adjacents = getAdjacents(grid, row, col)
    id = ""
    for elmnt in adjacents:
        if elmnt == None:
            id += "0"
        else:
            id += "1"
    return id


def getDoorOpenings(id, width, height):
    result = {}
    if id[0] == "1":
        result["up"] = [width / 2, height * 1 / 13]
    if id[1] == "1":
        result["down"] = [width / 2, height * (12 / 13) + 1]
    if id[2] == "1":
        result["left"] = [64, height / 2]
    if id[3] == "1":
        result["right"] = [width - 64, height / 2]
    return result
