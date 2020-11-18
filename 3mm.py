#!/usr/bin/env python3

from tkinter import *
import random
import aimodule as ai

class TMM(Tk):

    edges = [{0,1}, {1,2}, {3,4}, {4,5}, {6,7}, {7,8}, {0,3}, {3,6},
             {1,4}, {4,7}, {2,5}, {5,8}, {0,4}, {2,4}, {6,4}, {8,4}]


    winners_blue = ((3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    winners_red  = ((0,1,2),(3,4,5),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
    edgeset = {frozenset(x) for x in edges}
    NOTOVER = 0
    BPLAYER = 1
    RPLAYER = 2
    TIEGAME = 3
    def __init__(self):
        self.parent = Tk.__init__(self)

# make lists of all 27 images: 9 for empty square, 9 for blue, 9 for red

        self.emptypix = []
        self.redpix   = []
        self.bluepix  = []
        for i in range(9):
            self.emptypix.append(PhotoImage(file=f"Images/x{i}.gif"))
            self.redpix.append(PhotoImage(file=f"Images/r{i}.gif"))
            self.bluepix.append(PhotoImage(file=f"Images/b{i}.gif"))

        self.board = [1,1,1,0,0,0,2,2,2]                  # starting board configuration
        self.blist = []                                   # list of buttons
        for i in range(9):
            if self.board[i] == 1:                        # 1 is blue
                bu = Button(self,image=self.bluepix[i])
            elif self.board[i] == 2:                      # 2 is red
                bu = Button(self,image=self.redpix[i])
            else:                                         # 0 is empty
                bu = Button(self,image=self.emptypix[i])
            bu.configure(command=lambda b=bu: self.click(b))   # the lambda trick: identify the button
            bu.position = i                                    # store button number in the object itself
            bu.grid(row=(i // 3), column=(i % 3))              # grid coordinates
            self.blist.append(bu)                              # append to button list

        self.moving = False      # start the game, moving is True after we pick the piece to move
        self.turn = 1            # blue moves first

    def chackgame(self):
        who = self.turn
        if who == 1:
            for pat in TMM.winners_blue:
                if all([self.baord[x]== who for x in pat]):
                    return who
        if who == 2:
            for pat in TMM.winners_red:
                if all([self.board[x]== who for x in pat]):
                    return who
        if 0 not in self.board:
            return TMM.TIEGAME
        return TTT.NOTOVER

# the do_move method is not called until we know the move is val
    def do_move(self,newpos,oldpos,who):
                                           # update the board
        self.board[newpos] = who
        if who == 1:
            self.blist[oldpos].configure(image=self.emptypix[oldpos])  # put empty image at old location
            self.board[oldpos] = 0  
            self.blist[newpos].configure(image=self.bluepix[newpos])
        else:
            movelist =[]
            i = random.choice([self.board[i]==2])
            self.blist[i].configure(image=self.emptypix[i])  # put empty image at old location
            self.board[i] = 0  
            movelist.append(j for {i,j} in TMM.edges) 
            self.blist[ai.phase4(self.board, 2, movelist)].configure(image=self.redpix[ai.phase4(self.board,2,movelist)])
        self.moving = False
        self.turn = 3 - self.turn
        
    def click(self, button):
        x = button.position                                # number of the button that was clicked
        if self.moving:
            if self.board[x] == 0 and {x,self.savepos} in TMM.edges:
                self.do_move(x, self.savepos, self.turn)
        else:
            if self.board[x] == self.turn:                 # need a reminder of old position
                self.savepos = x
                self.moving = True              

if __name__ == "__main__":

    game = TMM()
    game.mainloop()
