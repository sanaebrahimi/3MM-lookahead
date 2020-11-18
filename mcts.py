#!/usr/bin/env python3

import gc               # garbage collecion
import sys
import numpy as np
import winners
from math import sqrt, log
from random import choice

class MCT:    # Monte Carlo Tree Search

    HUGE = 1e9
    winlist, windict = winners.getall()
    nodecount = 0

    def __init__(self, board, ptr, who):
        self.who    = who                 # who moves from this position
        self.board  = np.copy(board)
        self.ptr    = [*ptr]
        self.points = 0
        self.ntimes = 0
        self.isleaf = True
        self.parent =  None
        self.child  = [None]*7
        self.depth  = 0
        self.id     = MCT.nodecount
        MCT.nodecount += 1

    def __str__(self):
        s = "\n"
        for i in range(1,-1,-1):
            s += str(self.board[i]) + "\n"
        s += "{0:d} {1:9.3f} {2:3d}".format(self.depth, self.points, self.ntimes)
        return s
    def validmove(self,):



    def markmove(self,k,who):
        self.board[self.ptr[k],k] = who
        self.ptr[k] += 1

    def expand(self):
        if not self.isleaf:
            print('expand: expanding a non leaf?', self, file=sys.stderr)
            sys.exit(0)
        self.isleaf = False
        for i in range(7):
            if self.board[5,i] == 0:    # or use ptr
                self.child[i] = MCT(self.board, self.ptr, 3-self.who)
                self.child[i].parent = self
                self.child[i].markmove(i, self.who)
                self.child[i].depth = self.depth + 1

    def rollout(self):
        b = np.copy(self.board)
        p = np.copy(self.ptr)
        w = self.who
        while True:
            m = choice([i for i in range(7) if p[i] < 6])
            r,c = p[m],m
            b[r,c] = w
            p[m] += 1
            f,x = MCT.gameover(b,(r,c),w)
            if f:
                break
            w = 3 - w
        return x

    def bestchild(self):
        for i in range(7):
            if self.child[i]:
                if self.child[i].ntimes == 0:
                    return i
        best = -1e9
        which = -1
        for i in range(7):
            if self.child[i]:
                t = self.child[i].goofyformula()
                if t > best:
                    best, which = t, i
        return which

    def getmovevalue(self):
        if self.isleaf:
            if self.ntimes > 0:
                self.expand()
                k = self.bestchild()
                v = self.child[k].getmovevalue()
            else:                                # the 'else' is for decoration
                v = self.rollout()
            if v > 0:
                xv = -1 if self.who == v else 1
                self.points = xv
        else:
            k = self.bestchild()
            if k < 0:
                print('getmovevalue: no children in nonleaf?', self, file=sys.stderr)
                sys.exit(0)
            v = self.child[k].getmovevalue()
            if v > 0:
                xv = -1 if self.who == v else 1
                self.points += xv 
        self.ntimes += 1
        return v
 
    def goofyformula(self):
        if not self.parent:
            return 0
        return self.points/self.ntimes + 3*sqrt(log(self.parent.ntimes)/self.ntimes)

    def traverse(self,n):
        s = "{0:4d} {1:4d} {2:7d} {3:7d} {4:12.6f} {5:d}".format(self.depth,
                self.id, self.parent.id, self.ntimes, self.points, self.who)
        print(s)
        for i in range(7):
            c = self.child[i]
            if c:
                c.traverse(i)

    @classmethod
    def gameover(cls,board, move, who):
        for k in cls.windict[move]:
            win = cls.winlist[k]
            if all( [board[i,j] == who for i,j in win] ):
                return True, who
        if any([board[5,i] == 0 for i in range(7)]):
            return False, None
        return True, 0

if __name__ == "__main__":

    b = np.zeros((6,7),dtype=np.uint8)
    ptr = [0]*7
    who = 1

    MCT.nodecount = 0
    N = 1000

    root = MCT(b,ptr,who)                # create root node of the MCT
    root.parent = root

    root.expand()
    for i in range(N):                   # find the best move N times
        root.getmovevalue()

    root.traverse(0)
    print('nodecount =',MCT.nodecount, file=sys.stderr)

    del root
    gc.collect()

    

