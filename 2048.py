import pygame
import random
import copy
import sys
import colours as c

pygame.init()
SQ_SIZE = 100
BUF = 5
mainScreen = pygame.display.set_mode((425, 525))
mainScreen.fill(c.SCORE_BG)
screen = pygame.surface.Surface((425, 425))
score = 0


def drawGUI(board):
    mainScreen.fill(c.SCORE_BG)
    screen.fill(c.GRID_COLOR)
    for row in range(4):
        for col in range(4):
            value = board[row][col]
            pygame.draw.rect(screen, c.CELL_COLORS[value], (
                BUF + (col * SQ_SIZE + col * BUF), BUF + (row * SQ_SIZE + row * BUF), SQ_SIZE, SQ_SIZE))
            font = pygame.font.Font(pygame.font.get_default_font(), c.CELL_NUMBER_FONTS[value])
            number_label = font.render(str(value), True, c.CELL_NUMBER_COLORS[value])
            if value < 10:
                xpad = 40
                ypad = 30
            elif value < 100:
                xpad = 25
                ypad = 32
            elif value < 1000:
                xpad = 15
                ypad = 35
            else:
                xpad = 10
                ypad = 35
            screen.blit(number_label, (col * (SQ_SIZE + BUF) + xpad, row * (SQ_SIZE + BUF) + ypad))
    # score
    font = pygame.font.Font(pygame.font.get_default_font(), 24)
    score_label = font.render("Score: " + str(score), True, (0, 0, 0))
    mainScreen.blit(score_label, (160, 30))
    mainScreen.blit(screen, (0, 100))
    pygame.display.update()


def createBoard():
    board = [[0] * 4 for i in range(4)]
    return board


def showBoard(board):
    '''function for printing board in terminal'''
    for row in range(4):
        print(board[row])
    print("")


def newTiles(board):
    listOfZerros = []
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                # tupple of zerro
                listOfZerros.append((row, col))
    if listOfZerros != []:
        pick = random.choice(listOfZerros)
        row, col = pick
        board[row][col] = random.choice([2, 4])


def left(board):
    for row in range(4):
        x = 0
        for i in range(4):
            if board[row][x] == 0:
                del board[row][x]
                board[row].append(0)
            else:
                x += 1


def sumLeft(board):
    global score

    for row in range(4):
        for col in range(3):
            if board[row][col] == board[row][col + 1]:
                score += board[row][col] * 2
                board[row][col] = board[row][col] * 2

                board[row][col + 1] = 0
    left(board)


def right(board):
    for row in range(4):
        x = 3
        for i in range(4):
            if board[row][x] == 0:
                del board[row][x]
                board[row].insert(0, 0)
            else:
                x -= 1


def sumRight(board):
    global score

    for row in range(4):
        for col in range(3, -1, -1):
            if board[row][col] == board[row][col - 1]:
                score += board[row][col] * 2
                board[row][col] = board[row][col] * 2
                board[row][col - 1] = 0
    right(board)


def up(board):
    for col in range(4):
        colList = []
        for i in range(4):
            colList.append(board[i][col])
        y = 0
        for i in range(4):
            if colList[y] == 0:
                del colList[y]
                colList.append(0)
            else:
                y += 1
        for i in range(4):
            board[i][col] = colList[i]


def sumUp(board):
    global score

    for col in range(4):
        for row in range(3, -1, -1):
            if board[row][col] == board[row - 1][col]:
                score += board[row][col] * 2
                board[row][col] = board[row][col] * 2
                board[row - 1][col] = 0
    up(board)


def down(board):
    for col in range(4):
        colList = []
        for i in range(4):
            colList.append(board[i][col])
        y = 3
        for i in range(4):
            if colList[y] == 0:
                del colList[y]
                colList.insert(0, 0)
            else:
                y -= 1
        for i in range(4):
            board[i][col] = colList[i]


def sumDown(board):
    global score

    for col in range(4):
        for row in range(3):
            if board[row][col] == board[row + 1][col]:
                score += board[row][col] * 2
                board[row][col] = board[row][col] * 2
                board[row + 1][col] = 0
    down(board)


def check(board):
    # if there is 2048 then you won
    for col in range(4):
        for row in range(4):
            if board[row][col] == 2048:
                font = pygame.font.Font(pygame.font.get_default_font(), 55)
                win_label = font.render("YOU WON!", True, (222, 84, 200))
                screen.blit(win_label, (70, 200))
                mainScreen.blit(screen, (0, 100))
                pygame.display.update()
                return True
    # if there is any 0 then there are moves
    for col in range(4):
        for row in range(4):
            if board[row][col] == 0:
                return True
    # check if there is any move left in cols
    for col in range(4):
        for row in range(3):
            if board[row][col] == board[row + 1][col]:
                return True
    # check if there is any move left in rows
    for row in range(4):
        for col in range(3):
            if board[row][col] == board[row][col + 1]:
                return True

    font = pygame.font.Font(pygame.font.get_default_font(), 55)
    lost_label = font.render("GAME OVER!", True, (222, 84, 200))
    screen.blit(lost_label, (40, 185))
    mainScreen.blit(screen, (0, 100))
    pygame.display.update()
    pygame.time.delay(5000)
    return False


def copyMatrix(board):
    copyBoard = board.copy()
    return copyBoard


game = createBoard()
newTiles(game)
newTiles(game)
drawGUI(game)
showBoard(game)

while check(game):
    oldGame = copy.deepcopy(game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left(game)
                sumLeft(game)
            if event.key == pygame.K_RIGHT:
                right(game)
                sumRight(game)
            if event.key == pygame.K_UP:
                up(game)
                sumUp(game)
            if event.key == pygame.K_DOWN:
                down(game)
                sumDown(game)
    newGame = copy.deepcopy(game)
    if newGame != oldGame:
        newTiles(game)
    drawGUI(game)
    showBoard(game)
