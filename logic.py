from operator import itemgetter
import math
import random

class Board:
    board = []
    indicators = []
    filledCells = []
    
    connect = 0
    height = 0
    length = 0

    def __init__(self, height, length, connect):
        self.connect = connect
        self.height = height
        self.length = length
        
        x = 0
        y = 0

        while x < height:
            row = []
            while y < length:
                row.append(0)
                y += 1
            self.board.append(row)
            x += 1
            y = 0

        while y < length:
            self.indicators.append(y + 1)
            y += 1
        
    def printBoard(self):
        for row in self.board:
            print(" "*16, end='')
            print(row)
        print("Column Numbers:", end=' ')
        print(self.indicators)

    def insertToken(self, insertionPosition, player):
        inserted = False
        y = len(self.board) - 1
        while y >= 0 and not inserted:
            if self.board[y][insertionPosition] == 0:
                self.board[y][insertionPosition] = player.number
                self.filledCells.append([insertionPosition, y, player.number])
                self.filledCells.sort()
                inserted = True
            y -= 1
        if inserted:
            self.printBoard()
        else:
            if not player.CPU:
                print("Column Full! Please reselect.")
    
    def newMove(self, player):
        if (player.CPU):
            print("Computer making move")
            insertionPosition = self.cpuInsert(player)
        else:
            insertionPosition = Input.askValue("Player " + str(player.number) + "'s column to place token: ", "Please enter a valid column (1 - " + str(len(self.board[0])) + ").", 1, len(self.board[0])) - 1
        
        self.insertToken(insertionPosition, player)
    
    def cpuInsert(self, cpuPlayer):
        availableColumns = []
        x = 0
        while x < len(self.board[0]):
            if self.board[0][x] == 0:
                availableColumns.append(x)
            x += 1
        pickedColumn = availableColumns[random.randint(0, len(availableColumns) - 1)]
        return pickedColumn
    
    def fullBoardChecker(self):
        full = False
        x = 0
        while not full and x < len(self.board[0]):
            if self.board[0][x] == 0:
                full = True
            x += 1
        return full

    def connectChecker(self):
        for cell in self.filledCells:
            connectList = []
            if cell[0] <= len(self.board[0]) - self.connect:
                connectList.append(self.connectTokens("horizontal", cell))
            if cell[1] <= len(self.board) - self.connect:
                connectList.append(self.connectTokens("vertical", cell))
            if cell[0] <= len(self.board[0]) - self.connect and cell[1] >= self.connect - 1:
                connectList.append(self.connectTokens("upwards diagonal", cell))
            if cell[0] <= len(self.board[0]) - self.connect and cell[1] <= len(self.board) - self.connect:
                connectList.append(self.connectTokens("downwards diagonal", cell))

            for connection in connectList:
                if connection[0]:
                    return connection

    def connectTokens(self, direction, basecell):
        adjacentCells = []
        adjacentCells.append(basecell)
        for cell in self.filledCells:
            conditional = self.passConditional(direction, cell, basecell)
            if conditional[0]:
                adjacentCells.append(cell)
                basecell = cell
        return [len(adjacentCells) >= self.connect, adjacentCells[0][2]]

    def passConditional(self, direction, cell, basecell):
        passConditional = False
        if cell[2] == basecell[2]:
            if (direction == "horizontal"):
                passConditional = cell[1] == basecell[1] and cell[0] == basecell[0] + 1
            elif (direction == "vertical"):
                passConditional = cell[0] == basecell[0] and cell[1] == basecell[1] + 1
            elif (direction == "upwards diagonal"):
                passConditional = cell[0] == basecell[0] + 1 and cell[1] == basecell[1] - 1
            elif (direction == "downwards diagonal"):
                passConditional = cell[0] == basecell[0] + 1 and cell[1] == basecell[1] + 1
        return [passConditional, cell[2]]

class SimBoard(Board):
    children = []
    nextPlayerNumber = 0

    def __init__(self, parent, nextPlayerNumber):
        Board.__init__(self, parent.height, parent.length, parent.connect)
        self.filledCells = parent.filledCells
        self.nextPlayerNumber = nextPlayerNumber

    def placeTokens(self):
        player = Player(nextPlayerNumber, True)
        x = 0
        while x < len(self.board[0]):
            if self.board[0][x] == 0:
                newBoard = SimBoard(self, 1)
                newBoard.insertToken(x, player)
                boardResult = newBoard.connectChecker()
                if (boardResult != None):
                    children.append([newBoard, boardResult[0], boardResult[1]])
                else:
                    newBoard.placeTokens
                    children.append([newBoard, False, None])        

class Player:
    number = 0
    CPU = False

    def __init__(self, number, CPU):
        self.number = number
        self.CPU = CPU

class Input:
    @staticmethod
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