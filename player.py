#!/usr/bin/env python3

from random import choice

MAXDEPTH = 6

edges = [{0,1}, {1,2}, {3,4}, {4,5}, {6,7}, {7,8}, {0,3}, {3,6},
         {1,4}, {4,7}, {2,5}, {5,8}, {0,4}, {2,4}, {6,4}, {8,4}]

edgeset = {frozenset(x) for x in edges}

winners = ( (0,1,2), (3,4,5), (2,4,6), (0,3,6),
            (1,4,7), (2,5,8), (0,4,8), (6,7,8) )

count = 0

def makemovelist(board, who):
    global edgeset

    fromlist = [x for x in range(9) if board[x] == who]
    tolist   = [x for x in range(9) if board[x] ==   0]
    movelist = [(f,t) for f in fromlist for t in tolist if frozenset({f,t}) in edgeset]
    return movelist

def boardvalue(board, who):
    global winners

    winlist = winners[1:] if who == 1 else winners[:-1]
    for pat in winlist:
        if all([board[x] == who for x in pat]):
            return who
    if len(makemovelist(board,-who)) == 0:
        return who
    return 0

def alpha(depth, board, who):    # alpha for player 1, beta for player -1 (aka 2)
    global count
    
    count += 1
    bcopy = [*board]
    mlist = makemovelist(board, who)
    best = -2
    for move in mlist:
        bcopy[move[0]], bcopy[move[1]] = bcopy[move[1]], bcopy[move[0]]
        val = boardvalue(bcopy, who)
        if depth < MAXDEPTH and val == 0:
            _, val = beta(depth+1, bcopy, -who)
        if val > best:
            best = val
            bestmove = move
        bcopy[move[0]], bcopy[move[1]] = bcopy[move[1]], bcopy[move[0]]
    return bestmove, best

def beta(depth, board, who):    # alpha for player 1, beta for player -1 (aka 2)
    global count
    
    count += 1
    bcopy = [*board]
    mlist = makemovelist(board, who)
    best =  2
    for move in mlist:
        bcopy[move[0]], bcopy[move[1]] = bcopy[move[1]], bcopy[move[0]]
        val = boardvalue(bcopy, who)
        if depth < MAXDEPTH and val == 0:
            _, val = alpha(depth+1, bcopy, -who)
        if val < best:
            best = val
            bestmove = move
        bcopy[move[0]], bcopy[move[1]] = bcopy[move[1]], bcopy[move[0]]
    return bestmove, best

def getmove(board, who):
    global edgeset
    global count

    count = 0                    # counting alpha + beta calls
    if who == 2:
        who = -1
    bcopy = [-1 if x == 2 else x for x in board]
    moves = makemovelist(bcopy, who)
    if len(moves) == 0:
        return None
    if who == 1:                               # blue
        move, best = alpha(0, bcopy, 1)
    else:
        move, best = beta(0, bcopy, -1)
    print('player thinks', move, 'has value', best)
    print('alpha and beta were called', count, 'times');
    return move

if __name__ == "__main__":

    pass

