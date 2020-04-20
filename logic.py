from operator import itemgetter
import math
import random

board = []
indicators = []
filledCells = []
moveNumber = 0
playerNumber = 1
connect = 0
cpuPlayer = False

def initialiser():
    global connect
    global cpuPlayer
    
    cpuPlayerInt = askValue("Number of players - 1 (vs CPU) or 2 (1 vs 1): ", "Please enter a number between 1 and 2", 1, 2)
    cpuPlayer = cpuPlayerInt == 1
    
    connect = askValue("How many tokens must be connected? ", "Please allow for at least 3 tokens to be connected", 3, math.inf)
    numberOfRows = askValue("Number of rows: ", "Minimum height of 4", 4, math.inf)
    numberOfColumns = askValue("Number of columns: ", "Minimum width of 4", 4, math.inf)

    x = 0
    y = 0

    while x < numberOfRows:
        row = []
        while y < numberOfColumns:
            row.append(0)
            y += 1
        board.append(row)
        x += 1
        y = 0

    while y < numberOfColumns:
        indicators.append(y + 1)
        y += 1

def askValue(question, errorMessage, minimum, maximum):
    try:
        value = int(input(question))
        while value < minimum or value > maximum:
            print(errorMessage)
            value = int(input(question))
        return value
    except (ValueError):
        print("Please enter an integer")
        return askValue(question, errorMessage, minimum, maximum)
    
def printBoard():
    for row in board:
        print(" "*16, end='')
        print(row)
    print("Column Numbers:", end=' ')
    print(indicators)

def insertToken():
    global moveNumber
    global playerNumber
    playerNumber = (moveNumber % 2) + 1

    if (cpuPlayer and playerNumber == 2):
        print("Computer making move")
        insertionPosition = cpuInsertToken()
    else:
        insertionPosition = askValue("Player " + str(playerNumber) + "'s column to place token: ", "Please enter a valid column (1 - " + str(len(board[0])) + ").", 1, len(board[0])) - 1
    
    inserted = False
    y = len(board) - 1
    while y >= 0 and not inserted:
        if board[y][insertionPosition] == 0:
            board[y][insertionPosition] = playerNumber
            filledCells.append([insertionPosition, y, playerNumber])
            filledCells.sort()
            inserted = True
        y -= 1
    if inserted:
        moveNumber += 1
        printBoard()
    else:
        if not (cpuPlayer and playerNumber == 2):
            print("Column Full! Please reselect.")

def cpuInsertToken():
    availableColumns = []
    x = 0
    while x < len(board[0]):
        if board[0][x] == 0:
            availableColumns.append(x)
        x += 1
    pickedColumn = availableColumns[random.randint(0, len(availableColumns) - 1)]
    return pickedColumn

def fullBoardChecker():
    full = False
    x = 0
    while not full and x < len(board[0]):
        if board[0][x] == 0:
            full = True
        x += 1
    return full

def continueGame():
    return fullBoardChecker() and not connectChecker()

def connectChecker():
    for cell in filledCells:
        horizontalConnect = cell[0] <= len(board[0]) - connect and connectTokens("horizontal", cell)
        verticalConnect = cell[1] <= len(board) - connect and connectTokens("vertical", cell)
        upwardsDiagonalConnect = cell[0] <= len(board[0]) - connect and cell[1] >= connect - 1 and connectTokens("upwards diagonal", cell)
        downwardsDiagonalConnect = cell[0] <= len(board[0]) - connect and cell[1] <= len(board) - connect and connectTokens("downwards diagonal", cell)
        if horizontalConnect or verticalConnect or upwardsDiagonalConnect or downwardsDiagonalConnect: 
            return True

def connectTokens(direction, basecell):
    adjacentCells = []
    adjacentCells.append(basecell)
    for cell in filledCells:
        if passConditional(direction, cell, basecell):
            adjacentCells.append(cell)
            basecell = cell
    return len(adjacentCells) >= connect

def passConditional(direction, cell, basecell):
    if (direction == "horizontal"):
        return cell[1] == basecell[1] and cell[0] == basecell[0] + 1 and cell[2] == basecell[2]
    elif (direction == "vertical"):
        return cell[0] == basecell[0] and cell[1] == basecell[1] + 1 and cell[2] == basecell[2]
    elif (direction == "upwards diagonal"):
        return cell[0] == basecell[0] + 1 and cell[1] == basecell[1] - 1 and cell[2] == basecell[2]
    elif (direction == "downwards diagonal"):
        return cell[0] == basecell[0] + 1 and cell[1] == basecell[1] + 1 and cell[2] == basecell[2]

initialiser()
printBoard()
while continueGame():
    insertToken()

gameOverString =  "Game Over ~"
if cpuPlayer and playerNumber == 2:
    gameOverString += "CPU Wins!~"
else:
    gameOverString += "Player " + str(playerNumber) + " wins!~"

print(gameOverString)