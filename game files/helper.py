import random
from cmu_112_graphics import *


def getFixedParentDir(parent_dir):
    result = ''
    for e in parent_dir:
        if e == '\\':
            result += '/'
            continue
        result += e
    return result


def getRandomLocation(borders, windowWidth, windowHeight):
    leftBorder, rightBorder = borders[0], borders[1]
    topBorder, botBorder = borders[2], borders[3]
    x = random.randint(leftBorder+240, rightBorder-240)
    y = random.randint(topBorder+240, botBorder-240)
    return x,y


def getCachedPhotoImage(image):
    if "cachedPhotoImage" not in image.__dict__:
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
    return image.cachedPhotoImage




