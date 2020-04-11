import random
import sudokuui
from tkinter import Tk

side, mini = 9, 3
mat = [ [0]*side for _ in range(side) ]
check = [ [0]*side for _ in range(side) ]

root = Tk()
window = sudokuui.SudokuUI(root, mat)

#Generating a sudoku question

def fillDiagonal():
    for i in range(0, side, mini):
        fillBox(i, i)

def unUsedInBox(rowStart, colStart, num):
    for i in range(mini):
        for j in range(mini):
            if mat[rowStart + i][colStart + j] == num:
                return False
    return True

def fillBox(row, col):
    for i in range(mini):
        for j in range(mini):
            while True:
                num = random.randint(0, side)
                if(unUsedInBox(row, col, num)):
                    break
            mat[row + i][col + j] = num

def checkIfSafe(i, j ,num):
    return (unUsedInRow(i, num) and
                unUsedInCol(j, num) and
                unUsedInBox(i - i % mini, j - j % mini, num))

def unUsedInRow(i, num):
    for j in range(side):
        if mat[i][j] == num:
            return False
    return True

def unUsedInCol(j, num):
    for i in range(side):
        if mat[i][j] == num:
            return False
    return True

def fillRemaining(i, j):
    if (j >= side and i < side - 1):
        i = i + 1
        j = 0
    if (i >= side and j >= side):
        return True
    if i < mini:
        if j < mini:
            j = mini
    elif i < (side - mini):
        if j == int((i // mini) * mini):
            j = j + mini
    else:
        if j == (side - mini):
            i = i + 1
            j = 0
            if i >= side:
                return True
    for num in range(1, 10):
        if checkIfSafe(i, j, num):
            mat[i][j] = num
            if(fillRemaining(i, j + 1)):
                return True
            mat[i][j] = 0
    return False

def removeDigits(window, tk):
    count = 55
    while (count != 0):
        cellId = random.randint(0, (side * side) - 1)
        i = (cellId // side)
        j = ((cellId % side) + 1)
        if j != 0:
            j = j - 1
        if mat[i][j] != 0:
            count = count - 1
            mat[i][j] = 0
            for i in range(2000000):
                pass
            window.redraw(mat)
            tk.update()
    check = mat

#Check if array is solvable


def find_empty_loc(grid, record):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                record[0] = row
                record[1] = col
                return True
    return False

def used_in_row(grid, row, num):
    for col in range(9):
        if grid[row][col] == num:
            return True
    return False

def used_in_col(grid, col, num):
    for row in range(9):
        if(grid[row][col] == num):
            return True
    return False

def used_in_box(grid, row, col, num):
    for box_row in range(3):
        starting_row_index = box_row + (row - row % 3)
        for box_col in range(3):
            starting_col_index = box_col + (col - col % 3)
            if grid[starting_row_index][starting_col_index] == num:
                return True
    return False

def check_proper_position(grid, row, col, num):
    return not used_in_row(grid, row, num) \
           and not used_in_col(grid, col, num) \
           and not used_in_box(grid, row, col, num)

def solve(grid):
    # Keep track of row and column indices
    record = [0, 0]

    if (not find_empty_loc(grid, record)):
        return True

    row = record[0]
    col = record[1]

    for num in range(1, 10):
        if check_proper_position(grid, row, col, num):
            # Attempt number placement
            grid[row][col] = num

            if (solve(grid)):
                return True

            # Reset if unsuccessful
            grid[row][col] = 0

    return False


def main():
    root.resizable(0,0)
    fillDiagonal()
    fillRemaining(0, mini)
    removeDigits(window, root)
    while True:
        if(solve(check)):
            break
        main()
    root.mainloop()

main()
