'''
Key:

-4 : Unclicked
-3 : Incorrectly flagged
-2 : Flagged
-1 : Bomb
0 - 8 : Numbers to draw

'''

import sys
import time
import random
import pygame


def CreateMap(width, height, defaultValue=0):
    map = []
    for i in range(height):
        map.append([])
        for j in range(width):
            map[i].append(defaultValue)
    return map

def PlaceBombs(map, numToPlace):
    placed = 0
    while placed < numToPlace:
        randomX = random.randint(0, width - 1)
        randomY = random.randint(0, height - 1)
        if map[randomY][randomX] != -1:
            map[randomY][randomX] = -1
            placed += 1
    return map

def FindNeighbours(x, y):
    neighbours = []
    for offset_x in range(-1, 2):
        for offset_y in range(-1, 2):
            if x + offset_x < width and x + offset_x >= 0 and y + offset_y < height and y + offset_y >= 0:
                neighbours.append((x + offset_x, y + offset_y))
    return neighbours

def PlaceNumbers(map):
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] != -1:
                continue
            neighbours = FindNeighbours(x, y)
            for neighbour in neighbours:
                if map[neighbour[1]][neighbour[0]] >= 0:
                    map[neighbour[1]][neighbour[0]] += 1

    return map

def ClickZeroes(x, y, visible, values):
    neighbours = FindNeighbours(x, y)
    for neighbour in neighbours:
        if visible[neighbour[1]][neighbour[0]] == -4:
            visible[neighbour[1]][neighbour[0]] = values[neighbour[1]][neighbour[0]]
            if values[neighbour[1]][neighbour[0]] == 0:
                ClickZeroes(neighbour[0], neighbour[1], visible, values)

def PrintMap(map):
    for line in map:
        print(line)

def RenderMap(map):
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] >= 0:
                pygame.draw.rect(screen, (50, 50, 50), (x * scale, y * scale, scale - 1, scale - 1), 0)
                if map[y][x] >= 1:
                    font = pygame.font.SysFont('monospace', scale)
                    text = font.render(str(map[y][x]), True, (0, 0, 0))
                    screen.blit(text, (x * scale + (text.get_rect().width / 2) - scale / 15, y * scale))
            elif map[y][x] == -4:
                pygame.draw.rect(screen, (100, 100, 100), (x * scale, y * scale, scale - 1, scale - 1), 0)
            elif map[y][x] == -2:
                pygame.draw.rect(screen, (255, 100, 100), (x * scale, y * scale, scale - 1, scale - 1), 0)
            elif map[y][x] == -3:
                pygame.draw.rect(screen, (100, 100, 100), (x * scale, y * scale, scale - 1, scale - 1), 0)
                pygame.draw.polygon(screen, (255, 100, 100), [(x * scale, y * scale), ((x + 1) * scale - 2, y * scale), (x * scale, (y + 1) * scale - 2)])
            elif map[y][x] == -1:
                pygame.draw.rect(screen, (0, 0, 0), (x * scale, y * scale, scale - 1, scale - 1), 0)

    pygame.display.update()

def DrawTime(startTime):
    pygame.draw.rect(screen, (200, 200, 200), (width * scale, 0, width * scale + sideMenuWidth, height * scale))
    font = pygame.font.SysFont('monospace', 50)
    elapsedTime = time.time() - startTime
    minutes = "0" if int(elapsedTime // 60) < 10 else ""
    minutes += str(int(elapsedTime // 60))
    seconds = "0" if int(elapsedTime % 60) < 10 else ""
    seconds += str(int(elapsedTime % 60))
    text = font.render(f"{minutes}:{seconds}", True, (0, 0, 0))
    screen.blit(text, (width * scale + (sideMenuWidth / 2 - text.get_rect().width/2), sideMenuWidth / 10))
    pygame.display.update()

def Lost():
    for y in range(len(values)):
        for x in range(len(values[y])):
            if values[y][x] == -1 and visible[y][x] != -2:
                visible[y][x] = -1
            elif visible[y][x] == -2 and values[y][x] != -1:
                visible[y][x] = -3
    
    RenderMap(visible)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

def Won():
    RenderMap(visible)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

def InitPygame():
    pygame.init()
    windowSize = scale * width + sideMenuWidth, scale * height
    screen = pygame.display.set_mode(windowSize)
    return screen    

def Initialise():
    values = CreateMap(width, height)
    values = PlaceBombs(values, numBombs)
    values = PlaceNumbers(values)

    visible = CreateMap(width, height, -4)
    return values, visible

def Play():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos = (pos[0]//scale, pos[1]//scale)

                if pos[0] < width and pos[1] < height:
                    if event.button == 1:
                        if visible[pos[1]][pos[0]] == -4:
                            visible[pos[1]][pos[0]] = values[pos[1]][pos[0]]
                            if values[pos[1]][pos[0]] == 0:
                                ClickZeroes(pos[0], pos[1], visible, values)
                            if values[pos[1]][pos[0]] == -1:
                                print('lost')
                                Lost()
                                return
                            
                    if event.button == 3:
                        if visible[pos[1]][pos[0]] == -4:
                            visible[pos[1]][pos[0]] = -2
                        elif visible[pos[1]][pos[0]] == -2:
                            visible[pos[1]][pos[0]] = -4

                    flagged = 0
                    unclicked = 0
                    for y in range(len(visible)):
                        for x in range(len(visible[y])):
                            if visible[y][x] == -2: flagged += 1
                            elif visible[y][x] == -4: unclicked += 1
                    
                    if unclicked != 0:
                        pass
                    elif flagged == numBombs:
                        print('won')
                        Won()
                        return

                if event.button == 2:
                    RenderMap(values)
                    time.sleep(2)
                
                RenderMap(visible)
        DrawTime(startTime)


width, height = 20, 20
sideMenuWidth = 200
difficulty = 3
numBombs = round(width * height * (0.015* difficulty + 0.1))
scale = min(1700 // width, 1000 // height)
screen = InitPygame()

while True:
    values, visible = Initialise()
    startTime = time.time()
    RenderMap(visible)
    DrawTime(startTime)
    Play()
