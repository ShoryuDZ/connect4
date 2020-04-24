from tkinter import *
from logic import *
import math

def initialiser():
    
    cpuPlayerInt = Input.askValue("Number of players - 1 (vs CPU) or 2 (1 vs 1): ", "Please enter a number between 1 and 2", 1, 2)
    
    player1 = Player(1, False)
    player2 = Player(2, cpuPlayerInt != 2)

    numberOfRows = Input.askValue("Number of rows: ", "Minimum height of 4", 4, math.inf)
    numberOfColumns = Input.askValue("Number of columns: ", "Minimum width of 4", 4, math.inf)
    connect = Input.askValue("How many tokens must be connected? ", "Please allow for between 3 and the board width tokens to be connected", 3, numberOfColumns)

    mainBoard = Board(numberOfRows, numberOfColumns, connect)

    return [player1, player2], mainBoard

def continueGame(board, players):
    winningPlayer = board.connectChecker()
    if board.fullBoardChecker() and winningPlayer == None:
        return True
    
    for player in players:
        if player.number == winningPlayer[1]:
            endGame(player)
            return False

def endGame(winningPlayer):
    gameOverString =  "Game Over ~"
    if winningPlayer.CPU:
        gameOverString += "CPU Wins!~"
    else:
        gameOverString += "Player " + str(winningPlayer.number) + " wins!~"

    print(gameOverString)

if __name__ == "__main__":
    players, mainBoard = initialiser()
    mainBoard.printBoard()
    lastMover = players[1]
    while continueGame(mainBoard, players):
        if (lastMover == players[1]):
            mainBoard.newMove(players[0])
            lastMover = players[0]
        else:
            mainBoard.newMove(players[1])
            lastMover = players[1]

""" 
def begin_game():
    print("No func here yet...")

window = Tk()
window.geometry("500x500")
window.title("Connect4 Player")

frame = Frame(window)
frame.pack()

slogan = Button(frame, text="Start", command=begin_game)
slogan.pack(side=LEFT)

window.mainloop() """