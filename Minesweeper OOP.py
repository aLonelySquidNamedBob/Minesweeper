import random
import time
import pygame, sys

class Node:
    def __init__(self, i, j, value=0):
        self.pos = (i, j)
        self.value = value
        self.clicked = False
        self.flagged = False
        self.clickable = True

def CreateMap():
    map = []
    for i in range(size[1]):
        map.append([])
        for j in range(size[0]):
            map[i].append(Node(i, j))
    return map

def FindNeighbours(map, node):
    i, j = node.pos
    iMin = max(0, i - 1)
    iMax = min(size[1], i + 1)
    jMin = max(0, j - 1)
    jMax = min(size[0], j + 1)
    neighbours = []
    for row in [row[jMin:jMax + 1] for row in map[iMin:iMax + 1]]:
        for neighbour in row:
            if neighbour.pos != (i, j):
                neighbours.append(neighbour)
    return neighbours

def UpdateMap(map):
    for i in range(size[1]):
        for j in range(size[0]):
            if map[i][j].value != -1:
                num = 0
                neighbours = FindNeighbours(map, map[i][j])
                for neighbour in neighbours:
                    if neighbour.value == -1:
                        num += 1
                map[i][j].value = num
    return map

def PlaceBombs(map, numToPlace=10):
    numPlaced = 0
    while numPlaced < numToPlace:
        i = random.randint(0, size[1] - 1)
        j = random.randint(0, size[0] - 1)
        if map[i][j].value != -1:
            map[i][j].value = -1
            numPlaced += 1

    # for i in range(size):
    #     for j in range(size):
    #         map[i][j].value = -1 if random.randint(0, 100) < percentage else 0
    return map, numPlaced

def PrintMap(map):
    for row in map:
        for node in row:
            print(node.value, end=", ")
        print()

def DrawMap(screen, map):
    for i in range(size[1]):
        for j in range(size[0]):
            if not map[i][j].clicked:
                if map[i][j].flagged:
                    pygame.draw.rect(screen, (255, 100, 100), (j * scale, i * scale, scale - 1, scale - 1), 0)
                else: 
                    pygame.draw.rect(screen, (100, 100, 100), (j * scale, i * scale, scale - 1, scale - 1), 0)
            else:
                pygame.draw.rect(screen, (50, 50, 50), (j * scale, i * scale, scale - 1, scale - 1), 0)
                if map[i][j].value == -1:
                    pygame.draw.rect(screen, (0, 0, 0), (j * scale, i * scale, scale - 1, scale - 1), 0)
                elif map[i][j].value == -2:
                    pygame.draw.polygon(screen, (255, 100, 100), [(j * scale, i * scale), ((j + 1) * scale - 1, i * scale), (j * scale, (i + 1) * scale - 1)])
                elif map[i][j].value != 0:
                    font = pygame.font.SysFont('monospace', scale)
                    text = font.render(str(map[i][j].value), True, (0, 0, 0))
                    screen.blit(text, (j * scale + (text.get_rect().width / 2) - scale / 15, i * scale))
            
    pygame.display.update()

def DrawTime(screen, startTime):
    pygame.draw.rect(screen, (200, 200, 200), (size[0] * scale, 0, size[0] * scale + sideMenuWidth, size[1] * scale))
    font = pygame.font.SysFont('monospace', 50)
    elapsedTime = time.time() - startTime
    minutes = "0" if int(elapsedTime // 60) < 10 else ""
    minutes += str(int(elapsedTime // 60))
    seconds = "0" if int(elapsedTime % 60) < 10 else ""
    seconds += str(int(elapsedTime % 60))
    text = font.render(f"{minutes}:{seconds}", True, (0, 0, 0))
    screen.blit(text, (size[0] * scale + (sideMenuWidth / 2 - text.get_rect().width/2), sideMenuWidth / 10))

def DrawPlayButton(screen):
    sideMargin = 20
    topMargin = 100
    buttonHeight = 50
    pygame.draw.rect(screen, (100, 100, 100), (size[0] * scale + sideMargin, topMargin, sideMenuWidth - 2 * sideMargin, buttonHeight))

def DrawMenu(screen, startTime):
    DrawTime(screen, startTime)
    # DrawPlayButton(screen)

    pygame.display.update()


def Setup(difficulty):
    map = CreateMap()
    map, numBombs = PlaceBombs(map, (0.02 * difficulty + 0.05) * size[0] * size[1])
    map = UpdateMap(map)
    return map, numBombs

def InitPygame():
    pygame.init()
    windowSize = scale * size[0] + sideMenuWidth, scale * size[1]
    screen = pygame.display.set_mode(windowSize)
    return screen

def ClickZeros(map, node):
    neighbours = FindNeighbours(map, node)
    for neighbour in neighbours:
        if not neighbour.clicked and neighbour.clickable:
            neighbour.clicked = True
            neighbour.clickable = False
            if neighbour.value == 0:
                ClickZeros(map, neighbour)

def Lost(screen, map):
    print("lost")
    for row in map:
        for node in row:
            if not node.flagged and node.value == -1:
                node.clicked = True
            elif node.flagged and node.value != -1:
                node.clicked = True
                node.value = -2
    DrawMap(screen, map)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

def Won(screen, map):
    print("won")
    DrawMap(screen, map)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

def Menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

def main():
    global size, scale, sideMenuWidth, screen
    size = (5, 5)
    scale = min(1700 // size[0], 1000 // size[1])
    difficulty = 10
    sideMenuWidth = 200
    screen = InitPygame()
    map, numBombs = Setup(difficulty)

    startTime = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        ### GAME LOOP ###

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos = (pos[0]//scale, pos[1]//scale)
            
                if pos[0] < len(map[0]):
                    if event.button == 1:
                        if map[pos[1]][pos[0]].clickable:
                            map[pos[1]][pos[0]].clicked = True
                            map[pos[1]][pos[0]].clickable = False
                            if map[pos[1]][pos[0]].value == 0:
                                ClickZeros(map, map[pos[1]][pos[0]])
                            elif map[pos[1]][pos[0]].value == -1:
                                Lost(screen, map)

                    elif event.button == 3:
                        if map[pos[1]][pos[0]].flagged:
                            map[pos[1]][pos[0]].flagged = False
                            map[pos[1]][pos[0]].clickable = True
                        elif map[pos[1]][pos[0]].clickable:
                            map[pos[1]][pos[0]].flagged = True
                            map[pos[1]][pos[0]].clickable = False

                numClickable = 0
                numFlagged = 0
                for row in map:
                    for node in row:
                        if node.clickable: numClickable += 1
                        if node.flagged: numFlagged += 1
                
                if numClickable == 0:
                    if numFlagged == numBombs:
                        Won(screen, map)
        
        DrawMap(screen, map)
        DrawMenu(screen, startTime)

if __name__ == "__main__":
    main()
