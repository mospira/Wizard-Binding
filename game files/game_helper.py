from enemy import *
from floor import *
from spell_class import *
from PC_class import *
import math

"""
These functions are for when the app is considered
in "menu state" or "paused state"

"""


def initMenuAssets(app):
    app.model1_cycle = initMenuAssetsHelper(app, "dark")["Down"]
    app.model1 = app.model1_cycle[0]
    app.model2_cycle = initMenuAssetsHelper(app, "light")["Down"]
    app.model2 = app.model2_cycle[0]
    app.instructions_img = app.loadImage(par_dir + "/menu.png")
    return (
        app.model1_cycle,
        app.model1,
        app.model2_cycle,
        app.model2,
        app.instructions_img,
    )


def initMenuAssetsHelper(app, color):
    spriteSheet = app.loadImage(par_dir + "/sprites/player_sprites/mage-{}.png".format(color))
    spriteStrips = dict([("Up", []), ("Down", []), ("Left", []), ("Right", [])])
    for dir in spriteStrips:
        spriteStrips[dir] += cropPlayerSpriteSheet(dir, spriteSheet)
    return spriteStrips


def isHovering(app, x, y):
    app.hover1 = math.dist((x, y), (app.width / 2 - 200, app.height / 2 - 100)) < 150
    app.hover2 = math.dist((x, y), (app.width / 2 + 200, app.height / 2 - 100)) < 150


def drawMenu(app, canvas):
    canvas.create_image(
        app.width / 2, app.height / 2, image=ImageTk.PhotoImage(app.instructions_img)
    )
    if app.hover1:
        canvas.create_image(
            app.width / 2 - 200,
            app.height / 2 - 100,
            image=ImageTk.PhotoImage(
                app.scaleImage(app.model1_cycle[app.count % 3], 3)
            ),
        )
    else:
        canvas.create_image(
            app.width / 2 - 200,
            app.height / 2 - 100,
            image=ImageTk.PhotoImage(app.scaleImage(app.model1, 3)),
        )
    if app.hover2:
        canvas.create_image(
            app.width / 2 + 200,
            app.height / 2 - 100,
            image=ImageTk.PhotoImage(
                app.scaleImage(app.model2_cycle[app.count % 3], 3)
            ),
        )
    else:
        canvas.create_image(
            app.width / 2 + 200,
            app.height / 2 - 100,
            image=ImageTk.PhotoImage(app.scaleImage(app.model2, 3)),
        )


"""

The following functions assist the base MVC model
and run only when the app is considered in "game state"

"""


def initPlayerSprites(app):  # Loads and crops player movement sprites
    player = app.player
    #   Creating a dictionary for the sprites
    spriteSheet = app.loadImage(player.sprSheet_dir)
    spriteStrips = dict([("Up", []), ("Down", []), ("Left", []), ("Right", [])])
    for dir in spriteStrips:
        spriteStrips[dir] += cropPlayerSpriteSheet(dir, spriteSheet)
    return spriteStrips


def initEnemySprites(app):  # Loads and crops enemy movement sprites
    spriteSheet = app.scaleImage(app.loadImage(getEnemySpritesheetDir()), 1.3)
    spriteStrips = dict([("Up", []), ("Down", []), ("Left", []), ("Right", [])])
    for dir in spriteStrips:
        spriteStrips[dir] += cropEnemySpriteSheet(dir, spriteSheet)
    return spriteStrips


def initFloor(app):
    floor = Floor(app.level)
    floorplan = floor.generateFloor(8, 8)
    initStages(app, floorplan)
    return floor, floorplan


def initStages(app, floorplan):
    length = len(floorplan)
    width = len(floorplan[0])
    for i in range(length):
        for j in range(width):
            if floorplan[i][j] != 0:
                stage = Stage(app.level, floorplan, i, j)
                stage.base_img = app.loadImage(stage.base_dir)
                stage.doors_img = app.loadImage(stage.doorTypeDir)
                for path in stage.walls_dirs:
                    stage.walls_imgs.append(app.loadImage(path))
                floorplan[i][j] = stage


def initDescendRoom(app):
    stages = app.floor.getAllStages(app.floorplan)
    for stage in list(stages):
        if stage.gridPos == (3, 3):
            stages.remove(stage)
    index = random.randint(0, len(stages) - 1)
    room = stages[index]
    room.stairs_x, room.stairs_y = getStairsCoords(app.width, app.height)
    room.stairs_img = app.scaleImage(app.loadImage(room.stairs_dir), 1.25)
    return room


def initNewFloor(app):
    app.level += 1
    app.floor, app.floorplan = initFloor(app)
    app.curr_stage = app.floor.curr_room
    app.pathfind_timer = 0
    app.pathfinders = set()
    app.descend_room = initDescendRoom(app)
    return


def movePlayer(app, direction):
    """
    It moves the player in the direction specified.
    
    :param app: The app object
    :param direction: The direction the player is moving in
    """
    player = app.player
    ms = player.ms
    if direction == "Up":
        app.spriteCount += 10
        player.y -= ms
        player.direction = direction
        player.hitbox[1] -= ms
        player.hitbox[3] -= ms
    if direction == "Down":
        app.spriteCount += 10
        player.y += ms
        player.direction = direction
        player.hitbox[1] += ms
        player.hitbox[3] += ms
    if direction == "Left":
        app.spriteCount += 10
        player.x -= ms
        player.direction = direction
        player.hitbox[0] -= ms
        player.hitbox[2] -= ms
    if direction == "Right":
        app.spriteCount += 10
        player.x += ms
        player.direction = direction
        player.hitbox[0] += ms
        player.hitbox[2] += ms


def validMove(app):
    player = app.player
    ms = player.ms
    left, right, top, bottom = app.borders
    screen_change_check = checkRoomTransition(app)
    if screen_change_check[0] == True:
        transitionRooms(app, screen_change_check[1])
        return
    if player.hitbox[0] < left:
        player.x += ms
        player.hitbox[0] += ms
        player.hitbox[2] += ms
    if player.hitbox[2] > right:
        player.x -= ms
        player.hitbox[2] -= ms
        player.hitbox[0] -= ms
    if player.hitbox[1] < top:
        player.y += ms
        player.hitbox[1] += ms
        player.hitbox[3] += ms
    if player.hitbox[3] > bottom:
        player.y -= ms
        player.hitbox[3] -= ms
        player.hitbox[1] -= ms


def checkRoomTransition(app):
    """
    It checks if the player is within 80 pixels of the door opening, and if so, returns True and the
    direction of the door.
    
    :param app: the app object
    :return: A tuple of two values.
    """
    player = app.player
    floorplan = app.floorplan
    row, col = app.floor.curr_room[0], app.floor.curr_room[1]
    exitPoints = getDoorOpenings(getID(floorplan, row, col), app.width, app.height)
    for key in exitPoints:
        if key == "left":
            if (
                player.hitbox[0] < exitPoints[key][0]
                and exitPoints[key][1] - 80 < player.y < exitPoints[key][1] + 80
            ):
                return True, key
        if key == "right":
            if (
                player.hitbox[2] > exitPoints[key][0]
                and exitPoints[key][1] - 80 < player.y < exitPoints[key][1] + 80
            ):
                return True, key
        if key == "up":
            if (
                player.hitbox[1] < exitPoints[key][1]
                and exitPoints[key][0] - 80 < player.x < exitPoints[key][0] + 80
            ):
                return True, key
        if key == "down":
            if (
                player.hitbox[3] > exitPoints[key][1]
                and exitPoints[key][0] - 80 < player.x < exitPoints[key][0] + 80
            ):
                return True, key
    return False, "None"


def transitionRooms(app, direction):
    floor, player = app.floor, app.player
    gx, gy = floor.curr_room
    curr_stage = app.floorplan[gx][gy]
    initPathfinders(app, curr_stage, gx, gy)
    if direction == "up":
        floor.curr_room[0] -= 1
        player.x, player.y = app.width / 2, app.height * (12 / 13) - 60
    elif direction == "down":
        floor.curr_room[0] += 1
        player.x, player.y = app.width / 2, app.height / 13 + 60
    elif direction == "left":
        floor.curr_room[1] -= 1
        player.x, player.y = app.width - 94, app.height / 2
    elif direction == "right":
        floor.curr_room[1] += 1
        player.x, player.y = 94, app.height / 2
    player.updateHitbox()
    spawnEnemies(app)
    app.curr_spells = set()


def spawnEnemies(app):
    """
    It spawns enemies in the current room if there are no enemies in the current room.
    
    :param app: the app object
    """
    gx, gy = app.floor.curr_room
    curr_stage = app.floorplan[gx][gy]
    if curr_stage.enemies == []:
        for i in range(curr_stage.num_enemies):
            x, y = getRandomLocation(app.borders, app.width, app.height)
            enemy = Enemy(x, y, gx, gy, app.level)
            curr_stage.enemies.append(enemy)
    app.start_enemy_spawn = True


def getNewSpellPos(spell):
    angle = spell.getOrientation()
    angle_radians = math.radians(angle)
    spell.y -= spell.ms * math.sin(angle_radians)
    spell.x += spell.ms * math.cos(angle_radians)
    return (spell.x, spell.y)


def castSpell(app, x, y):
    """
    It creates a spell object, loads the image, and adds it to a sprite group
    
    :param app: the app object
    :param x: x-coordinate of the mouse
    :param y: The y-coordinate of the mouse
    """
    player = app.player
    if app.casting == False:
        spellName = player.spells[player.curr_spell_index]
        spr_dir = getDirectory(spellName)
        coords = [player.x, player.y, x, y]
        spell = Spell(spellName, player.x, player.y, spr_dir, coords)
        spell.image = app.loadImage(spell.sprSheet_dir).rotate(spell.getOrientation())
        app.curr_spells.add(spell)
        app.casting = True
        player.spells_cast += 1


def checkSpellBorders(app, spells_list):
    """
    It checks if the spell is within the borders of the screen, and if it is, it checks if it's in the
    hitbox of an enemy. If it is, it deals damage to the enemy
    
    :param app: the main app
    :param spells_list: a list of all the spells currently in the game
    """
    player = app.player
    gx, gy = app.floor.curr_room
    curr_stage = app.floorplan[gx][gy]
    left, right, top, bottom = app.borders
    for spell in set(spells_list):
        if spell.x < left or spell.x > right:
            try:
                spells_list.remove(spell)
            except:
                pass
        if spell.y < top or spell.y > bottom:
            try:
                spells_list.remove(spell)
            except:
                pass
        for enemy in curr_stage.enemies:
            if spell.inHitbox(enemy.x, enemy.y):
                enemy.takeDamage(spell.dmg)


def initPathfinders(app, stage, gx, gy):
    """
    It takes a stage, and a grid coordinate, and then it takes all the enemies in the stage and adds
    them to a list of pathfinders
    
    :param app: the app object
    :param stage: the stage that the enemy is in
    :param gx: the x coordinate of the stage that the enemy is in
    :param gy: the y coordinate of the stage that the enemy is in
    """
    floorplan = app.floorplan
    if stage.num_enemies > 0:
        homestage = floorplan[gx][gy]
        homestage.num_enemies -= 1
        for enemy in stage.enemies:
            app.pathfinders.add((enemy, (gx, gy)))


def transitionRooms(app, direction):
    floor, player = app.floor, app.player
    gx, gy = floor.curr_room
    curr_stage = app.floorplan[gx][gy]
    initPathfinders(app, curr_stage, gx, gy)
    if direction == "up":
        floor.curr_room[0] -= 1
        player.x, player.y = app.width / 2, app.height * (12 / 13) - 60
    elif direction == "down":
        floor.curr_room[0] += 1
        player.x, player.y = app.width / 2, app.height / 13 + 60
    elif direction == "left":
        floor.curr_room[1] -= 1
        player.x, player.y = app.width - 94, app.height / 2
    elif direction == "right":
        floor.curr_room[1] += 1
        player.x, player.y = 94, app.height / 2
    player.updateHitbox()
    spawnEnemies(app)
    app.curr_spells = set()


def checkSpawnEnemies(app):
    gx, gy = app.floor.curr_room
    curr_stage = app.floorplan[gx][gy]
    app.start_enemy_spawn = curr_stage.num_enemies > 0


def updateEnemyProps(app):
    """
    If an enemy's hp is less than or equal to 0, remove it from the current stage, update the number of
    enemies in the enemy's homestage, and increment the player's enemies_slain attribute
    
    :param app: the main app
    """
    player, floorplan = app.player, app.floorplan
    gx, gy = app.floor.curr_room
    curr_stage = app.floorplan[gx][gy]
    for enemy in list(curr_stage.enemies):
        gx, gy = enemy.homestage
        if enemy.hp <= 0:
            curr_stage.enemies.remove(enemy)
            floorplan[gx][gy].updateEnemies(-1)
            player.enemies_slain += 1
            continue
        enemy.updateDirection(player.x, player.y)
        enemy.sprite_count += 10


def updateHPSprite(app):
    app.hp_sprite = app.loadImage(app.player.getHP_spr_dir())


def checkPlayerEnemyCollisions(app):
    """
    If the player is not invincible, check if the player is within a certain distance of any enemies in
    the current room. If so, damage the player and make them invincible
    
    :param app: the app object
    :return: the value of the variable "player"
    """
    player = app.player
    if player.invinc_state == True:
        return
    gx, gy = app.floor.curr_room
    curr_stage = app.floorplan[gx][gy]
    hitDist = math.hypot(32, 65)
    for enemy in curr_stage.enemies:
        dist = math.dist((enemy.x, enemy.y), (player.x, player.y))
        if dist < hitDist:
            player.takeDamage(1)
            updateHPSprite(app)
            player.invinc_state = True
            break


def checkPlayerInvinc(app):
    player = app.player
    if player.invinc_state == True:
        player.invinc_count += 25
    if player.invinc_count == 100:
        player.invinc_state = False
        player.invinc_count = 0


def updatePathfind(app):
    """
    It's a function that updates the pathfinding of enemies in a game.
    
    :param app: the app
    """
    app.pathfind_timer += 10
    floorplan, floor = app.floorplan, app.floor
    for item in set(app.pathfinders):
        target = floor.curr_room
        enemy = item[0]
        if enemy.path == None:
            start = item[1]
            enemy.path = enemy.getPath(floorplan, start, target)
        if getPathfindChance(app.pathfind_timer):
            if enemy.path == []:
                continue
            enemy.path.pop(0)
            if enemy.path == []:
                continue
            gx, gy = enemy.path[0][0], enemy.path[0][1]
            if [gx, gy] == target:
                enemy.x, enemy.y = getRandomLocation(app.borders, app.width, app.height)
                curr_stage = floorplan[gx][gy]
                curr_stage.enemies.append(enemy)
                enemy.updateHitbox()
                curr_stage.updateEnemies(1)
                app.pathfinders.remove(item)
            else:
                floorplan[gx][gy].updateEnemies(1)


def checkDescension(app):
    player, floorplan = app.player, app.floorplan
    gx, gy = app.floor.curr_room
    curr_stage = floorplan[gx][gy]
    if (
        curr_stage == app.descend_room
        and curr_stage.inDescendRange(player.x, player.y)
        and app.floor.getTotalEnemies(floorplan) == 0
    ):
        initNewFloor(app)


def checkSpellCooldown(app):
    if app.casting == True:
        app.spell_cd += 10
    if app.spell_cd == 100:
        app.casting = False
        app.spell_cd = 0


def performGameChecks(app):
    """
    It checks if the player is invincible, if the enemies should spawn, if the enemies should move, if
    the player should move, if the player should cast a spell, and if the spell should move
    
    :param app: the main app
    """
    checkSpawnEnemies(app)
    checkDescension(app)
    updateEnemyProps(app)
    checkPlayerEnemyCollisions(app)
    checkPlayerInvinc(app)
    updatePathfind(app)
    checkSpellCooldown(app)
    checkSpellBorders(app, app.curr_spells)


def drawPlayer(app, canvas):
    direction = app.player.direction
    image = app.player_sprites[direction][app.spriteCount % 3]
    image = getCachedPhotoImage(image)
    canvas.create_image(app.player.x, app.player.y, image=image)


def drawSpells(
    app,
    canvas,
):
    for i in app.curr_spells:
        spell = i
        image = app.scaleImage(spell.image, 0.13)
        x, y = getNewSpellPos(spell)
        image = getCachedPhotoImage(image)
        canvas.create_image(x, y, image=image)  # ImageTk.PhotoImage(image))


def drawHP(app, canvas):
    player = app.player
    image = app.hp_sprite
    image = app.scaleImage(image, 1)
    canvas.create_image(player.x, player.y - 40, image=ImageTk.PhotoImage(image))


def drawStage(app, canvas):
    floorplan = app.floorplan
    stage = floorplan[app.curr_stage[0]][app.curr_stage[1]]
    base = stage.base_img
    base = getCachedPhotoImage(base)
    canvas.create_image(
        app.width / 2, app.height / 2, image=base
    )  # ImageTk.PhotoImage(base))


def drawWalls(app, canvas):
    floorplan = app.floorplan
    stage = floorplan[app.curr_stage[0]][app.curr_stage[1]]
    for img in stage.walls_imgs:
        img = getCachedPhotoImage(img)
        canvas.create_image(
            app.width / 2, app.height / 2, image=img
        )  # ImageTk.PhotoImage(img))


def drawStageDecor(app, canvas):
    floorplan = app.floorplan
    stage = floorplan[app.curr_stage[0]][app.curr_stage[1]]
    for img in stage.deco_imgs:
        image = img[0]
        x, y = img[1]
        canvas.create_image(x, y, image=ImageTk.PhotoImage(image))


def drawExit(app, canvas):
    gx, gy = app.floor.curr_room
    curr_stage = app.floorplan[gx][gy]
    if curr_stage == app.descend_room:
        img = getCachedPhotoImage(app.descend_room.stairs_img)
        canvas.create_image(curr_stage.stairs_x, curr_stage.stairs_y, image=img)


def drawEnemies(app, canvas):
    gx, gy = app.floor.curr_room
    curr_stage = app.floorplan[gx][gy]
    if app.start_enemy_spawn == True:
        for enemy in curr_stage.enemies:
            image = app.enemy_sprites[enemy.direction][enemy.sprite_count % 3]
            image = getCachedPhotoImage(image)
            canvas.create_image(enemy.x, enemy.y, image=image)
            # canvas.create_rectangle(enemy.x-17, enemy.y - 35, enemy.x + 17, enemy.y + 35)


def drawDoors(app, canvas):
    floorplan = app.floorplan
    stage = floorplan[app.curr_stage[0]][app.curr_stage[1]]
    doors = stage.doors_img
    doors = getCachedPhotoImage(doors)
    canvas.create_image(app.width / 2, app.height / 2, image=doors)


def drawAnalytics(app, canvas):
    player = app.player
    canvas.create_text(
        player.x,
        player.y + 50,
        font=("I pixel u", "10"),
        fill="white",
        text="ENEMIES SLAIN: {}\n SPELLS CAST: {}\n FLOOR: {}".format(
            player.enemies_slain, player.spells_cast, app.level
        ),
    )


def drawGameFunctions(app, canvas):
    drawStage(app, canvas)
    drawExit(app, canvas)
    drawWalls(app, canvas)
    drawPlayer(app, canvas)
    drawEnemies(app, canvas)
    drawSpells(app, canvas)
    drawDoors(app, canvas)
    drawHP(app, canvas)
    if app.stats:
        drawAnalytics(app, canvas)
    return
