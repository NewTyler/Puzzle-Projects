from boards import *
import random

#print_board
#inputs   : board - sudoku board
#outputs  : None
#function : traverses the board list and prints out the sudoku board
#           formatted accordingly
def print_board(board):

    for row in range(len(board)):
        if ((row % 3) == 0 and (row != 0)):
            print("- - - - - - - - - - - - - ")
        for col in range(len(board[row])):
            if ((col % 3) == 0 and (col != 0)):
                print(" | "  + " ", end="")
            if (col == 8):
                print(board[row][col])
                break
            print(str(board[row][col]) + " ", end = "")


#solve_sudoku
#inputs   : board - sudoku board
#outputs  : True if successful, false if there is no solution
#function : Backtracking algorithm that attempts to solve the board
#           
def solve_sudoku(board):

    open_spot = find_blank(board)
    if (open_spot == None):
        print("Sudoku Solved")
        print_board(board)
        return board
    
    row, col = open_spot
    to_use_nums = [1,2,3,4,5,6,7,8,9]
    used_nums = []

    for i in range(9):

        cur_num = random.choice(to_use_nums)
        while cur_num in used_nums:
            cur_num = random.choice(to_use_nums)
        used_nums.append(cur_num)

        if check_move(board, cur_num, (row,col)):
            board[row][col] = cur_num

            if solve_sudoku(board):
                return True
            
            board[row][col] = 0
    
    return False


#find_blank
#inputs   : board - sudoku board
#outputs  : the location of the first blank found, or None if completed
#function : Traverses the board searching for a blank space, returning the location of
#           the first blank cell 
def find_blank(board):

    for row in range(len(board)):
        for col in range(len(board[row])):
            if (board[row][col] == 0):
                return (row, col)

    return None


#check_move
#inputs   : board - sudoku board
#         : move  - the number that is being guessed 
#         : pos   - row,col that is to be checked
#outputs  : False if the move is not valid
#         : True if tthe move is valid
#function : checks that the current guess in the position selected
#           is a valid guess
def check_move(board, move, pos):

    #row check
    for i in range(len(board[pos[0]])):
        if ((board[pos[0]][i] == move) and (pos[1] != i)):
            return False
    #col check
    for j in range(len(board)):
        if ((board[j][pos[1]] == move) and (pos[0] != j)):
            return False

    #box check
    #print('box_check')
    box_row = int((pos[0] / 3)) * 3
    box_col = int((pos[1] / 3)) * 3
    #print( 'current pos : ' + str(pos))

    for row in range(3):
        for col in range(3):
            #print('column : ' + str(box_col) + ' ' + str(col))
            #print('row : ' + str(box_row) + ' ' + str(row))
            if ((board[box_row + row][box_col + col] == move) and ((box_row+row,box_col+col) != pos)):
                return False

    return True


print_board(board1)
solve_sudoku(board1)
