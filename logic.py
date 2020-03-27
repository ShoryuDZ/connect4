numberOfRows = int(input("How many rows on the board? "))
numberOfColumns = int(input("How many columns on the board? "))

x = 0
y = 0
board = []

while x < numberOfRows:
    row = []
    while y < numberOfColumns:
        row.append(0)
        y += 1
    board.append(row)
    print(board[x])
    x += 1
    y = 0