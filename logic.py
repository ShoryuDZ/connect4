from operator import itemgetter
import math
import random

class Board:
    board = []
    indicators = []
    filledCells = []
    connect = 0

    def __init__(self, height, length, connect):
        self.connect = connect
        
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
            insertionPosition = self.cpuInsert()
        else:
            insertionPosition = Input.askValue("Player " + str(player.number) + "'s column to place token: ", "Please enter a valid column (1 - " + str(len(self.board[0])) + ").", 1, len(self.board[0])) - 1
        
        self.insertToken(insertionPosition, player)
    
    def cpuInsert(self):
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
            horizontalConnect = cell[0] <= len(self.board[0]) - self.connect and self.connectTokens("horizontal", cell)
            verticalConnect = cell[1] <= len(self.board) - self.connect and self.connectTokens("vertical", cell)
            upwardsDiagonalConnect = cell[0] <= len(self.board[0]) - self.connect and cell[1] >= self.connect - 1 and self.connectTokens("upwards diagonal", cell)
            downwardsDiagonalConnect = cell[0] <= len(self.board[0]) - self.connect and cell[1] <= len(self.board) - self.connect and self.connectTokens("downwards diagonal", cell)
            if horizontalConnect or verticalConnect or upwardsDiagonalConnect or downwardsDiagonalConnect: 
                return True

    def connectTokens(self, direction, basecell):
        adjacentCells = []
        adjacentCells.append(basecell)
        for cell in self.filledCells:
            if self.passConditional(direction, cell, basecell):
                adjacentCells.append(cell)
                basecell = cell
        return len(adjacentCells) >= self.connect

    def passConditional(self, direction, cell, basecell):
        if (direction == "horizontal"):
            return cell[1] == basecell[1] and cell[0] == basecell[0] + 1 and cell[2] == basecell[2]
        elif (direction == "vertical"):
            return cell[0] == basecell[0] and cell[1] == basecell[1] + 1 and cell[2] == basecell[2]
        elif (direction == "upwards diagonal"):
            return cell[0] == basecell[0] + 1 and cell[1] == basecell[1] - 1 and cell[2] == basecell[2]
        elif (direction == "downwards diagonal"):
            return cell[0] == basecell[0] + 1 and cell[1] == basecell[1] + 1 and cell[2] == basecell[2]

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