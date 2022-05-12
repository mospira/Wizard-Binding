from game_helper import *
from cmu_112_graphics import *
from enemy import *
from floor import *
from spell_class import *
from PC_class import *

par_dir = os.path.dirname(os.path.realpath(__file__))


#   Model
def appStarted(app):
    #   Values for the menu
    app.game_state = False
    [
        app.model1_cycle,
        app.model1,
        app.model2_cycle,
        app.model2,
        app.instructions_img,
    ] = initMenuAssets(app)
    app.hover1, app.hover2 = False, False
    app.pc_color = None
    app.count = 0

    #   Initialize player/enemy object and assets
    app.player = PC(app.width / 2, app.height / 2)
    app.player_sprites = None
    app.enemy_sprites = initEnemySprites(app)
    app.hp_sprite = app.loadImage(app.player.getHP_spr_dir())
    app.level = 1

    #   Keeps track of player movement states
    app.spriteCount = 0

    #   All spells the player has cast which should be rendered
    app.curr_spells = set()
    app.casting = False
    app.spell_cd = 0
    app.mouse_pos = ()

    #   Initializes the first floor/level available to the player
    app.floor, app.floorplan = initFloor(app)

    #   Keeps track of which room of the level the player is in
    app.curr_stage = app.floor.curr_room

    #   Maintains enemy spawning and pathfinding
    app.start_enemy_spawn = True
    app.pathfind_timer = 0
    app.pathfinders = set()

    #   Identifies which room contains a descending staircase to the next floor
    app.descend_room = initDescendRoom(app)

    #   Bool value for whether to view player stats or not
    app.stats = False

    app.borders = [64, app.width - 64, app.height * (1 / 13), app.height * 12 / 13]
    return


# Controller
def mousePressed(app, event):
    if app.game_state:
        castSpell(app, event.x, event.y)
    if not app.game_state:
        if app.hover1:
            app.pc_color = "dark"
            app.game_state = True
            app.player.updateSprSheetDir(app.pc_color)
            app.player_sprites = initPlayerSprites(app)
        elif app.hover2:
            app.pc_color = "light"
            app.game_state = True
            app.player.updateSprSheetDir(app.pc_color)
            app.player_sprites = initPlayerSprites(app)


def mouseMoved(app, event):
    if not app.game_state:
        isHovering(app, event.x, event.y)
    if app.game_state:
        app.mouse_pos = (event.x, event.y)


def keyPressed(app, event):
    if app.game_state:
        if event.key == "w":
            movePlayer(app, "Up")
            validMove(app)
        if event.key == "s":
            movePlayer(app, "Down")
            validMove(app)
        if event.key == "a":
            movePlayer(app, "Left")
            validMove(app)
        if event.key == "d":
            movePlayer(app, "Right")
            validMove(app)
        if event.key == "Space":
            app.stats = not app.stats


def timerFired(app):
    if app.hover1 or app.hover2:
        app.count += 10
    if app.game_state:
        performGameChecks(app)


#   View
def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="black")
    if not app.game_state:
        drawMenu(app, canvas)
    if app.game_state:
        drawGameFunctions(app, canvas)

    return


#   Running the app
runApp(width=1024, height=832)
