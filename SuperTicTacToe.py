import pygame
from collections import Counter

#setting up window
pygame.init()

display_height = 804  #display only needs one value since it's a square
#for some reason if the length isn't a multiple of 6 it won't work correctly. Probably, due to rounding

#getting color examples
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


gameDisplay = pygame.display.set_mode((display_height, display_height))

pygame.display.set_caption('Super Tic Tac Toe')
def lines(d):
    lines = [2 * d // 3, d // 3]
    return lines

clock = pygame.time.Clock()
clock.tick(60) #60 updates per second

#these help find the points that are in the upper left-hand corner of each square (needs to be made into a function to be used in super board)
twoThird = 2 * display_height // 3
oneThird = display_height // 3

def drawBoard(startX, startY, d): #makes board

    for line in lines(d):
        pygame.draw.line(gameDisplay, white,(line, startY), (line, d), 1)
        pygame.draw.line(gameDisplay, white, (startX ,line), (d, line), 1)

def mouseInSquare(): #outputs the point in the upper left-hand corner for aa reference for the x's and circles.

    right = mousex > 2 * display_height // 3
    left = mousex < display_height // 3
    middlex = mousex > display_height // 3 and mousex < 2 * display_height // 3
    up = mousey < display_height // 3
    middley = mousey < 2 * display_height // 3 and mousey > display_height // 3
    down = mousey > 2 * display_height // 3

    if right and up:
        location = [twoThird, 0]
    elif middlex and up:
        location = [oneThird, 0]
    elif left and up:
        location = [0, 0]
    elif right and middley:
        location = [twoThird, oneThird]
    elif middlex and middley:
        location = [oneThird, oneThird]
    elif left and middley:
        location = [0,oneThird]
    elif right and down:
        location = [twoThird, twoThird]
    elif middlex and down:
        location = [oneThird, twoThird]
    elif left and down:
        location = [0, twoThird]
    else:
        location = [3,3]
    print(location)
    return location

def drawx(list):
    if list != [3,3]:
        x = list[0]
        y = list[1]
        pygame.draw.line(gameDisplay, blue, (x,y), (x + oneThird, y + oneThird))
        pygame.draw.line(gameDisplay, blue, (x + oneThird, y), (x, y + oneThird))

def drawCircle(list):
    if list != [3,3]:
        x = list[0]
        y = list[1]
        pygame.draw.circle(gameDisplay, red, (x + oneThird // 2, y + oneThird // 2), oneThird // 2, 1)

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

    print('coords')
    print(record)
    return win




turn = 0
xRecords = []
circleRecords = []
stop = False
while not stop:

    for event in pygame.event.get():


        if event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if turn % 2 == 0 and mouseInSquare() not in circleRecords and mouseInSquare() not in xRecords: #x's turn
                drawx(mouseInSquare())
                turn += 1
                xRecords.append(mouseInSquare())

            elif turn % 2 != 0 and mouseInSquare() not in xRecords and mouseInSquare() not in circleRecords: #circle's turn
                drawCircle(mouseInSquare())
                turn += 1
                circleRecords.append(mouseInSquare())

            if threeRow(xRecords) == True: #x wins
                gameDisplay.fill(white)

            elif threeRow(circleRecords) == True: #circle wins
                gameDisplay.fill(green)

            elif len(xRecords) + len(circleRecords) == 9: #tie
                gameDisplay.fill(black)

        drawBoard(0, 0, display_height)
        pygame.display.flip()
        if event.type == pygame.QUIT:
            stop = True