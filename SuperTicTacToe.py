import pygame
from collections import Counter

#setting up window
pygame.init()
level = 2
display_height = 1000  #display only needs one value since it's a square
#for some reason if the length isn't a multiple of 6 it won't work correctly. Probably, due to rounding

#getting color examples
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


gameDisplay = pygame.display.set_mode((display_height, display_height))

pygame.display.set_caption('Super Tic Tac Toe')

clock = pygame.time.Clock()
clock.tick(60) #60 updates per second

#these help find the points that are in the upper left-hand corner of each square (needs to be made into a function to be used in super board)
twoThird = 2 * display_height // 3
oneThird = display_height // 3


def setPoints(lv):  # outputs locations based on their level. These are the upper right-hand corners of the squares.
    points = []
    for n in range(1, 3 ** lv):
        points.append(n * display_height // 3 ** lv)
    #print(points)
    return points


def topLeftPoints(x):
    list1 = []
    i = 0
    for n in range(0, 3 ** x):
        if n != 0:
            i = n * display_height // 3 ** x
        else:
            i = 0
        for n in range(0, 3 ** x):
            if n != 0:
                j = n * display_height // 3 ** x
            else:
                j = 0

            list1.append([i, j])
    return list1


def allTopLeftPoints(lv):
    list2 = []
    for x in reversed(range(1, lv + 1)):
        list2.append(topLeftPoints(x))
    return list2


def drawBoard(lv): #makes board
    points = setPoints(lv)
    for x in reversed(range(1, lv + 1)):
        if x == 1:
            color = white
        elif x % 2 == 0:
            color = green
        elif x % 3 == 0:
            color = red
        else: color = blue
        for p in setPoints(x):
            pygame.draw.line(gameDisplay, color,(p, 0), (p, display_height), 1)
            pygame.draw.line(gameDisplay, color, (0, p), (display_height, p), 1)

def mouseInSquare(lv):
    for point in allTopLeftPoints(lv)[0]:
        if mousex > point[0] and mousex < point[0] + display_height // 3 ** lv:
            if mousey > point[1] and mousey < point[1] + display_height // 3 ** lv:
                return point
    return [3,3]
def mouseInSquare2(lv, x, y):
    for point in allTopLeftPoints(lv)[0]:
        if x > point[0] and x < point[0] + display_height // 3 ** lv:
            if y > point[1] and y < point[1] + display_height // 3 ** lv:
                return point


def drawx(list, lv):
    if list != [3,3]:
        x = list[0]
        y = list[1]
        pygame.draw.line(gameDisplay, blue, (x,y), (x + oneThird // 3 ** (lv - 1), y + oneThird // 3 ** (lv - 1)))
        pygame.draw.line(gameDisplay, blue, (x + oneThird // 3 ** (lv - 1), y), (x, y + oneThird // 3 ** (lv - 1)))

def drawCircle(list, lv):
    if list != [3,3]:
        x = list[0]
        y = list[1]
        pygame.draw.circle(gameDisplay, red, (x + oneThird // 2 // 3 ** (lv - 1), y + oneThird // 2 // 3 ** (lv - 1)), oneThird // 2 // 3 ** (lv - 1), 1)

def threeRow(record):
    win = False
    xcoord = []
    ycoord = []
    for coord in record:
        xcoord.append(coord[0])
        ycoord.append(coord[1])
    xCount = Counter(xcoord)
    for x in xCount.values():
        if x == 3:
            win = True
    yCount = Counter(ycoord)
    for y in yCount.values():
        if y == 3:
            win = True
    counter = 0
    for coord in record:
        if coord[0] == coord[1]:
            counter += 1
            if counter == 3:
                win = True
    counter2 = 0
    for coord in record:
        if abs(coord[0] - twoThird) == coord[1]:
            counter2 += 1
            if counter2 == 3:
                win = True
    return win

turn = 0
xRecords = []
circleRecords = []
allRecords = []
stop = False
while not stop:

    for event in pygame.event.get():

        if event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if len(xRecords) == 0:

                if turn % 2 == 0 and mouseInSquare(level) not in circleRecords and mouseInSquare(level) not in xRecords: #x's turn
                    drawx(mouseInSquare(level), level)
                    turn += 1
                    xRecords.append(mouseInSquare(level))
                    allRecords.append(mouseInSquare(level))

                elif turn % 2 != 0 and mouseInSquare(level) not in xRecords and mouseInSquare(level) not in circleRecords: #circle's turn
                    drawCircle(mouseInSquare(level), level)
                    turn += 1
                    circleRecords.append(mouseInSquare(level))
                    allRecords.append(mouseInSquare(level))

                if threeRow(xRecords) == True: #x wins
                    gameDisplay.fill(white)

                elif threeRow(circleRecords) == True: #circle wins
                    gameDisplay.fill(green)

                elif len(xRecords) + len(circleRecords) == 9: #tie
                    gameDisplay.fill(black)
            else:
                req = mouseInSquare2(level, allRecords[(turn - 1)][0] + 1, allRecords[(turn - 1)][1] + 1)
                req2 = mouseInSquare2(level - 1, allRecords[(turn - 1)][0] + 1, allRecords[(turn - 1)][1] + 1)

                xReqLower = (req[0] - req2[0]) * 3 ** (level - 1)
                yReqLower = (req[1] - req2[1]) * 3 ** (level - 1)

                xReqUpper = xReqLower + display_height // 3 ** (level - 1)
                yReqUpper = yReqLower + display_height // 3 ** (level - 1)

                #print("between" + str(xReq) + " and " + str(xReq + display_height // 3 ** (level - 1)))
                #print("between" + str(yReq) + " and " + str(yReq + display_height // 3 ** (level - 1)))

                if xReqLower < mousex and mousex < xReqUpper and yReqLower < mousey and mousey < yReqUpper:

                    if turn % 2 == 0 and mouseInSquare(level) not in circleRecords and mouseInSquare(level) not in xRecords:  # x's turn
                        drawx(mouseInSquare(level), level)
                        turn += 1
                        xRecords.append(mouseInSquare(level))
                        allRecords.append(mouseInSquare(level))

                    elif turn % 2 != 0 and mouseInSquare(level) not in xRecords and mouseInSquare(level) not in circleRecords:  # circle's turn
                        drawCircle(mouseInSquare(level), level)
                        turn += 1
                        circleRecords.append(mouseInSquare(level))
                        allRecords.append(mouseInSquare(level))

                    if threeRow(xRecords) == True:  # x wins
                        gameDisplay.fill(blue)

                    elif threeRow(circleRecords) == True:  # circle wins
                        gameDisplay.fill(red)

                    elif len(xRecords) + len(circleRecords) == 1000:  # tie
                        gameDisplay.fill(black)
        #drawBoard(oneThird, oneThird, oneThird, green)
        drawBoard(level)

        pygame.display.flip()
        if event.type == pygame.QUIT:
            stop = True