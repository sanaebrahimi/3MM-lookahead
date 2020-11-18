#!/usr/bin/env python3

import sys
from random import choice

count = 0

NOTDONE = 99

squareorder = [4, 0, 2, 6, 8, 1, 3, 5, 7]
squarevalue = [2, 1, 2, 1, 3, 1, 2, 1, 2]

# pattern means row, column, diagonal

def phase1(board, who):
    moves = [x for x in range(9) if board[x] == 0]
    return choice(moves)

def phase2(board, who):
    opp = 3 - who          # opp is the other player
#
# first check if we can win
#
    for pat in winners:
        s = [board[x] for x in pat]    # values in the square for this pattern
        if opp in s:                   # is the other play in this pattern
            continue
        if len([x for x in pat if board[x] == who]) == 2:
            return pat[s.index(0)]
#
# next check if we can prevent the other player from winning
#
    for pat in winners:
        s = [board[x] for x in pat]    # values in the square for this pattern
        if who in s:                   # is the other play in this pattern
            continue
        if len([x for x in pat if board[x] == opp]) == 2:
            return pat[s.index(0)]
    for x in squareorder:
        if board[x] == 0:
            return x
    print("Error in phase2: no available moves?", file=sys.stderr)
    return -1

def boardvalue(board, who):
    total = 0
#
# does 'who' have 3-in-a-row ?
#
    for pat in winners:
        tmp = {board[x] for x in pat}
        if len(tmp) == 1 and who in tmp:
            total += who * 1000
#
# does -who have an open 2-in-a-row
#
    for pat in winners:
        tmp = [board[x] for x in pat]
        if who not in tmp:
            if sum([x == -who for x in tmp]) == 2:
                total += -who * 100
#
# points for occupying squares
#
    total += sum([squarevalue[x] * board[x] for x in board])
    return total
 
def phase3(board, who):
    bcopy = [-1 if x == 2 else x for x in board]  # copy board, change 2's to -1's
    if who == 2:
        who = -1
    movelist = [x for x in range(9) if board[x] == 0]  # list of available moves
    value = {}
    for move in movelist:
        bcopy[move] = who
        value[move] = boardvalue(bcopy, who)
        bcopy[move] = 0
    fun = max if who == 1 else min                             # make fun either max or min
    return fun(list(value.keys()), key = lambda x: value[x])   #find the best x based on value[x]


# alpha-beta pruning version

def boardscore(board, who):
    for pat in winners:
        tmp = {board[x] for x in pat}
        if len(tmp) == 1 and who in tmp:
            return who
    if 0 not in board:
        return 0
    return NOTDONE

def alpha(board):     # considering X's moves
    global count

    count += 1
    movelist = [i for i in range(9) if board[i] == 0]
    bestmove, bestval = -1, -2
    for move in movelist:
        board[move] = 2
        val = boardscore(board, 2)
        if val == NOTDONE:
            _ , val = beta(board)
        if val > bestval:
            bestmove, bestval = move, val
        board[move] = 0
    return bestmove, bestval

def beta(board):     # considering O's moves
    movelist = [i for i in range(9) if board[i] == 0]
    bestmove, bestval = -1,  2
    for move in movelist:
        board[move] = -1
        val = boardscore(board, -1)
        if val == NOTDONE:
            _ , val = alpha(board)
        if val < bestval:
            bestmove, bestval = move, val
        board[move] = 0
    return bestmove, bestval

def phase4(board, who):
    global count

    count = 0
    bcopy = [x for x in board]  # copy board, change 2's to -1's
    if who == 1:
        bestmove, bestval = alpha(bcopy)
    #else:
    #    bestmove, bestval = beta(bcopy)
    print(count,'boards evaluated')
    return bestmove

#if __name__ == "__main__":

   # board = [1, 1, 0, -1, -1, 0, 0, 0, 0]
   # print(phase4(board,1))

