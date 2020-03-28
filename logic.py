board = []
indicators = []

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
    insertionPosition = int(input("Column to place token: ")) - 1
    
    inserted = False
    y = len(board) - 1
    while y >= 0 and not inserted:
        if board[y][insertionPosition] == 0:
            board[y][insertionPosition] = 1
            inserted = True
        y -= 1
    if inserted:
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

initialiser()
printBoard()
while fullBoardChecker():
    insertToken()

print("Game Over!")