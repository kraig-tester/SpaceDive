import pygame
from random import randint

pygame.init()

screenWidth = 400
screenHeight = 600

screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("Space Dive")

starship = pygame.image.load('assets/starship.png')
laser = pygame.image.load('assets/lazer.png')
beam = pygame.image.load('assets/beam.png')
shieldImage = pygame.image.load('assets/shield.png')
beamDrop = pygame.image.load('assets/beamDrop.png')
minigunDrop = pygame.image.load('assets/minigunDrop.png')
enemy1 = pygame.image.load('assets/enemy.png')
enemyBall = pygame.image.load('assets/enemyBall.png')
bg = pygame.image.load('assets/background.jpg')
bgHeight = -1000
bgHeight2 = -2600
bgVel = 1

black = (0,0,0)
clock = pygame.time.Clock()
x, y = 170, 500
width, height, vel, shootCooldown, shield, iFrames = 60, 60, 8, 0, 100, 0
bulletX, bulletY, bulletType = [], [], []
weapons = ['l','b','m']
currentBulletType = weapons[0]
bulletWidth, bulletHeight, bulletAmount, bulletVel = 30, 30, 0, 10
beamWidth, beamHeight = 25, 590
beamActive = False
bonusX, bonusY, bonusWidth, bonusHeight = None, None, 50, 50
currentBonusType, bonusImage, bonusWeaponFuel, bonusDrop, bonusVel =  None, None, 0, 100, 2
bonusList = ['b','m']
enemyBulletX, enemyBulletY = [], []
enemyBulletWidth, enemyBulletHeight, enemyBulletVel, enemyBulletAmount = 30, 30, 5, 0
enemyShootingSpeedLine = [60, 80, 100]
enemyShootingSpeedZ = [50, 100, 150]
currentShootingSpeed = 0
enemiesX, enemiesY, enemyMovementStyle, enemyDirection = [], [], [], []
enemyLine = [1,2,3]
enemyWidth, enemyHeight, enemyVel = 60, 50, 2
enemyCount, enemyWave = 0, 0
waveSpeed = [400,450,500,550]
currentWaveSpeed = 0
spawnPosition = 0
waveAmount, waveCount, waveCooldown = 0, 0, 0
spawnWave, spawnBonus = False, False

#optimized variables
bulletPoint, enemyBulletPoint = int(bulletWidth / 2), int(enemyWidth / 2)
enemyLinearRemoveLine, enemyZRemoveLineRight, enemyZRemoveLineLeft = (screenHeight + 100), (screenWidth + 100), (-enemyWidth - 40)
dropEndLine = screenWidth-100
bulletRemoveLine = (screenHeight + enemyBulletHeight)
oneEnemyLineSpawnX1 = (int(screenWidth / 2 * 1) - 30)
twoEnemyLineSpawnX1, twoEnemyLineSpawnX2 = (int(screenWidth / 4 * 1) - 30), (int(screenWidth / 4 * 3) - 30)
threeEnemyLineSpawnX1, threeEnemyLineSpawnX2 = (int(screenWidth / 6 * 1) - 30), (int(screenWidth / 6 * 3) - 30)
threeEnemyLineSpawnX3 = (int(screenWidth / 6 * 5) - 30)
fourEnemyLineSpawnX1, fourEnemyLineSpawnX2  = (int(screenWidth / 8 * 1) - 30), (int(screenWidth / 8 * 3) - 30)
fourEnemyLineSpawnX3, fourEnemyLineSpawnX4 = (int(screenWidth / 8 * 5) - 30), (int(screenWidth / 8 * 7) - 30)


"""Main drawing Function."""
def redrawGameWindow():
    global bulletAmount, enemyBulletAmount, beamActive, enemyCount, currentShootingSpeed, beam
    global bonusX, bonusY, iFrames
    i, e, k = 0, 0, 0

    redrawBackground()

    if iFrames <= 0:
        screen.blit(starship, (x, y))
    elif iFrames > 0:
        screen.blit(starship, (x, y))
        screen.blit(shieldImage, (x-22, y-20))
        iFrames -= 1
    #drawing bullets
    while i < bulletAmount:
        if bulletAmount > 0:
            screen.blit(laser, (bulletX[i], bulletY[i]))
            bulletY[i] -= bulletVel
        if bulletY[i] < 0 - bulletHeight or enemyKill(bulletX[i], bulletY[i]):
            del bulletX[i]
            del bulletY[i]
            del bulletType[i]
            i -= 1
            bulletAmount -= 1
        i += 1
    #drawing beam
    if currentBulletType == weapons[1] and beamActive:
        screen.blit(beam, (x-6, y - beamHeight))
        if bonusWeaponFuel%10 == 0:
            beam = pygame.transform.flip(beam, True, False)
        enemyKill(x+14, y)
        beamActive = False
    #drawing enemies
    while e < enemyCount:
        screen.blit(enemy1, (enemiesX[e], enemiesY[e]))
        if enemyMovementStyle[e] == 'l':
            enemiesY[e] += enemyVel
            if enemiesY[e]%currentShootingSpeed == 0 and enemiesY[e] > 0:
                shootEnemies(enemiesX[e], enemiesY[e])
            if enemiesY[e] > (enemyLinearRemoveLine):
                deleteEnemy(e)
                continue
        elif enemyMovementStyle[e] == 'z1':
            enemiesX[e] += enemyVel
            enemiesY[e] += enemyVel*enemyDirection[e]
            if enemiesY[e] > spawnPosition + 60 or enemiesY[e] < spawnPosition:
                enemyDirection[e] = -enemyDirection[e]
            if waveCooldown == 0 and enemiesX[e] < screenWidth:
                shootEnemies(enemiesX[e], enemiesY[e])
            if enemiesX[e] > (enemyZRemoveLineRight):
                deleteEnemy(e)
                continue
        elif enemyMovementStyle[e] == 'z2':
            enemiesX[e] -= enemyVel
            enemiesY[e] += enemyVel*enemyDirection[e]
            if enemiesY[e] > spawnPosition + 60 or enemiesY[e] < spawnPosition:
                enemyDirection[e] = -enemyDirection[e]
            if waveCooldown == 0 and enemiesX[e] > 0:
                shootEnemies(enemiesX[e], enemiesY[e])
            if enemiesX[e] < (enemyZRemoveLineLeft):
                deleteEnemy(e)
                continue
        e += 1
    #drawing enemy bullets
    while k < enemyBulletAmount:
        screen.blit(enemyBall, (enemyBulletX[k] + 23, enemyBulletY[k]))
        enemyBulletY[k] += enemyBulletVel
        if enemyBulletY[k] > (bulletRemoveLine) or shipHit(enemyBulletX[k], enemyBulletY[k]):
            del enemyBulletX[k]
            del enemyBulletY[k]
            k -= 1
            enemyBulletAmount -= 1
        k += 1
    #drawing bonus
    if bonusX != None:
        screen.blit(bonusImage, (bonusX, bonusY))
        bonusY += bonusVel
        if (bonusY + bonusHeight) > y and bonusY < (y + height) and bonusX < (x + width) and (bonusX + bonusWidth) > x:
            activateBonus()
        elif bonusY > screenHeight:
            bonusX = None
            bonusY = None
            bonusDrop = 2000
    pygame.display.update()


"""Draws background"""
def redrawBackground():
    global bgHeight, bgHeight2
    screen.blit(bg, (0, bgHeight))
    screen.blit(bg, (0, bgHeight2))
    if bgHeight2 == 0:
        bgHeight = -1600
    elif bgHeight == 0:
        bgHeight2 = -1600
    bgHeight2 += bgVel
    bgHeight += bgVel


"""Makes starship shoot current bullet type"""
def shootStarship():
    global bulletAmount
    if currentBulletType == weapons[0] or currentBulletType == weapons[2]:
        bulletX.append(x + 14)
        bulletY.append(y - 10)
        bulletType.append(currentBulletType)
        bulletAmount += 1


"""Spawns enemy with given attributes"""
def enemySpawn(X, Y, Movement, Direction):
    global enemyCount
    enemiesX.append(X)
    enemiesY.append(Y)
    enemyMovementStyle.append(Movement)
    enemyDirection.append(Direction)
    enemyCount += 1


"""Creates enemy bullets, based on their location"""
def shootEnemies(enemyX, enemyY):
    global enemyBulletAmount
    enemyBulletX.append(enemyX)
    enemyBulletY.append(enemyY)
    enemyBulletAmount +=1


"""Clears killed or fled enemies. Returns index updated index value"""
def deleteEnemy(index):
    global enemyCount
    del enemiesX[index]
    del enemiesY[index]
    del enemyMovementStyle[index]
    del enemyDirection[index]
    enemyCount -= 1


"""Adds enemy row based on amount
Temporary prototype"""
def addEnemyRow(enemyPos):
    global enemyWave, enemyLine
    if enemyPos == enemyLine[0]:
        enemySpawn(oneEnemyLineSpawnX1, -60, 'l', 1)
    elif enemyPos == enemyLine[1]:
        enemySpawn(twoEnemyLineSpawnX1, -60, 'l', 1)
        enemySpawn(twoEnemyLineSpawnX2, -60, 'l', 1)
    elif enemyPos == enemyLine[2]:
        enemySpawn(fourEnemyLineSpawnX1, -60, 'l', 1)
        enemySpawn(fourEnemyLineSpawnX2, -60, 'l', 1)
        enemySpawn(fourEnemyLineSpawnX3, -60, 'l', 1)
        enemySpawn(fourEnemyLineSpawnX4, -60, 'l', 1)
    enemyWave += 1
    """
    elif enemyPos == enemyLine[1]:
        enemySpawn(threeEnemyLineSpawnX1, -60, 'l', 1)
        enemySpawn(threeEnemyLineSpawnX2, -60, 'l', 1)
        enemySpawn(threeEnemyLineSpawnX3, -60, 'l', 1)
    """


"""Adds enemy zigzag lines
Temporary prototype"""
def addEnemyZigZag():
    global enemyWave
    enemySpawn(-enemyWidth, spawnPosition, 'z1', 1)
    enemySpawn(screenWidth, spawnPosition, 'z2', 1)
    enemyWave += 1


def shipHit(enemyX, enemyY):
    global shield, iFrames
    bulletCenter = enemyX + enemyBulletPoint
    if bulletCenter > x and enemyY > y and bulletCenter < x + width and enemyY < y + height and iFrames == 0:
        shield -= 25
        iFrames = 120
        print(shield)
        return True
    else:
        return False


"""Function takes starship bullet coordinates and removes enemy ship on bullet point match with front surface of it
Returns True on hit, False on miss"""
def enemyKill(hitX, hitY):
    global enemyCount, enemyWidth, enemyHeight, bulletWidth
    if currentBulletType == weapons[0] or currentBulletType == weapons[2]:
        bulletCenter = hitX + bulletPoint
        e = 0
        while e < enemyCount:
            if enemiesX[e] <= bulletCenter and (enemiesX[e] + enemyWidth) >= bulletCenter and enemiesY[e] <= hitY and (enemiesY[e] + enemyHeight) >= hitY:
                deleteEnemy(e)
                return True
            e += 1
        return False
    elif currentBulletType == weapons[1]:
        e = 0
        while e < enemyCount:
            if (enemiesX[e] + enemyWidth) >= hitX and enemiesX[e] <= (hitX+beamWidth) and enemiesY[e] < y:
                deleteEnemy(e)
                return True
            e += 1
        return False


"""Activates bonus on pick up"""
def activateBonus():
    global bonusWeaponFuel, currentBulletType, bonusX, bonusY, bonusDrop
    bonusWeaponFuel = 250
    currentBulletType = currentBonusType
    bonusX = None
    bonusY = None
    bonusDrop = 2000


running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            #temp
            if event.key == pygame.K_p:
                bonusWeaponFuel = 250
                currentBulletType = weapons[1]
            elif event.key == pygame.K_o:
                bonusWeaponFuel = 250
                currentBulletType = weapons[2]

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and x < (screenWidth - 10 - width):
        x += vel
    if keys[pygame.K_LEFT] and x > 10:
        x -= vel
    if keys[pygame.K_UP] and y > height:
        y -= vel
    if keys[pygame.K_DOWN] and y < (screenHeight - height - 10):
        y += vel
    if keys[pygame.K_SPACE]:
        if currentBulletType == weapons[0]:
            if shootCooldown <= 0:
                shootStarship()
                shootCooldown = 20
        elif currentBulletType == weapons[1]:
            if bonusWeaponFuel <= 0:
                currentBulletType = weapons[0]
                shootCooldown = 20
            else:
                bonusWeaponFuel -= 1
                beamActive = True
        elif currentBulletType == weapons[2]:
            if bonusWeaponFuel <= 0:
                currentBulletType = weapons[0]
            elif shootCooldown <= 0:
                shootStarship()
                shootCooldown = 8
            bonusWeaponFuel -= 1
    shootCooldown -= 1
    #enemy spawns
    if waveCooldown <= 0 and spawnWave and enemyWave <= waveAmount:
        if movementType == 1:
            addEnemyRow(randint(1,3))
        elif movementType == 2:
            addEnemyZigZag()
        if enemyWave == waveAmount:
            spawnWave = False
            waveAmount = 0
    elif enemyCount == 0 and not spawnWave:
        spawnWave = True
        waveCooldown = 1000
        currentWaveSpeed = waveSpeed[randint(0,3)]
        enemyWave = 0
        waveAmount = randint(4, 10)
        waveCount += 1
        movementType = randint(1,2)
        if movementType == 1:
            currentShootingSpeed = enemyShootingSpeedLine[(randint(0,2))]
        elif movementType == 2:
            currentShootingSpeed = enemyShootingSpeedZ[(randint(0,2))]
        print(currentShootingSpeed)
        spawnPosition = randint(60, 120)
    if waveCooldown <= 0:
        waveCooldown = currentWaveSpeed
    waveCooldown -= 10
    #bonus drop
    if bonusDrop == 0:
        bonusX = randint(40, dropEndLine)
        bonusY = -60
        currentBonusType = bonusList[randint(0,1)]
        if currentBonusType == bonusList[0]:
            bonusImage = beamDrop
        elif currentBonusType == bonusList[1]:
            bonusImage = minigunDrop
        bonusDrop = 2000
    bonusDrop -= 2
    #iFrame management
    redrawGameWindow()

pygame.quit()
