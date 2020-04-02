from operator import itemgetter

board = []
indicators = []
filledCells = []
moveNumber = 0
playerNumber = 1
connect = int(input("How many tokens must be connected? "))

def initialiser():
    numberOfRows = int(input("How many rows on the board? "))
    numberOfColumns = int(input("How many columns on the board? "))

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
    insertionPosition = int(input("Player " + str(playerNumber) + "'s column to place token: ")) - 1
    
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
        print("Column Full! Please reselect.")

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
        if (cell[0] <= len(board[0]) - connect and horizontalConnect(cell)) or (cell[1] <= len(board) - connect and verticalConnect(cell)) or (cell[0] <= len(board[0]) - connect and cell[1] >= connect - 1 and upwardsDiagonalConnect(cell)) or ((cell[0] <= len(board[0]) - connect and cell[1] <= len(board) - connect and downwardsDiagonalConnect(cell))): 
            return True

def horizontalConnect(basecell):
    horizontalCells = []
    horizontalCells.append(basecell)
    for cell in filledCells:
        if cell[1] == basecell[1] and cell[0] == basecell[0] + 1 and cell[2] == basecell[2]:
                horizontalCells.append(cell)
                basecell = cell
    return len(horizontalCells) >= connect

def verticalConnect(basecell):
    verticalCells = []
    verticalCells.append(basecell)
    for cell in filledCells:
        if cell[0] == basecell[0] and cell[1] == basecell[1] + 1 and cell[2] == basecell[2]:
            verticalCells.append(cell)
            basecell = cell
    return len(verticalCells) >= connect


def upwardsDiagonalConnect(basecell):
    diagonalCells = []
    diagonalCells.append(basecell)
    for cell in filledCells:
        if cell[0] == basecell[0] + 1 and cell[1] == basecell[1] - 1 and cell[2] == basecell[2]:
            diagonalCells.append(cell)
            basecell = cell
    return len(diagonalCells) >= connect

def downwardsDiagonalConnect(basecell):
    diagonalCells = []
    diagonalCells.append(basecell)
    for cell in filledCells:
        if cell[0] == basecell[0] + 1 and cell[1] == basecell[1] + 1 and cell[2] == basecell[2]:
            diagonalCells.append(cell)
            basecell = cell
    return len(diagonalCells) >= connect


initialiser()
printBoard()
while continueGame():
    insertToken()

print("Game Over ~Player " + str(playerNumber) + " wins!~")