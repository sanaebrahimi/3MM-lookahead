#!/usr/bin/env python3

from tkinter import *
import player

class TMM(Tk):

    edges = [{0,1}, {1,2}, {3,4}, {4,5}, {6,7}, {7,8}, {0,3}, {3,6},
             {1,4}, {4,7}, {2,5}, {5,8}, {0,4}, {2,4}, {6,4}, {8,4}]

    winners = ( (0,1,2), (3,4,5), (2,4,6), (0,3,6),
                (1,4,7), (2,5,8), (0,4,8), (6,7,8) )

    messagelist = ["", "Blue Wins", "Red Wins"]

    def __init__(self):
        self.parent = Tk.__init__(self)

        self.emptypix = []
        self.redpix   = []
        self.bluepix  = []
        for i in range(9):
            self.emptypix.append(PhotoImage(file=f"C:\\Users\\sebrahimi\\Documents\\x{i}.gif"))
            self.redpix.append(PhotoImage(file=f"C:\\Users\\sebrahimi\\Documents\\r{i}.gif"))
            self.bluepix.append(PhotoImage(file=f"C:\\Users\\sebrahimi\\Documents\\b{i}.gif"))

        self.gameover = False
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

        self.message = Label(text="", width=13, font=("Helvetica",42))
        self.message.grid(row=3, column=0, columnspan=3)

        self.moving = False      # start the game, moving is True after we pick the piece to move
        self.turn = 1            # blue moves first
        tmp = player.getmove(self.board, self.turn)   # after we move, the computer moves immediately
        self.do_move(tmp[1], tmp[0], self.turn)

#
# Determine if 'who' cannot make a valid move, in which case the other player wins.
#
    def cantmove(self, who):

        for e in TMM.edges:                                # for each edge
            x,y = list(e)                                  # can't get set elements by coordinate, so make it a list
            if {self.board[x], self.board[y]} == {0,who}:  # is this a value, one 'who' and one empty
                return False
        return True

#
# the boardvalue == the player who just moved if they have a valid three in a row, or ...
# if the other player can't move
#

    def boardvalue(self):

        winlist = TMM.winners[1:] if self.turn == 1 else TMM.winners[:-1]   # winlist isn't the same for each player
        for pat in winlist:
            if all([self.board[x] == self.turn for x in pat]):     # three in a row for self.turn
                return self.turn
        if self.cantmove(3 - self.turn):                           # other player can't move
            return self.turn
        return 0

# the do_move method is not called until we know the move is valid

    def do_move(self,newpos,oldpos,who):
        self.blist[oldpos].configure(image=self.emptypix[oldpos])  # put empty image at old location
        self.board[oldpos] = 0                                     # update the board
        self.board[newpos] = who
        if who == 1:
            self.blist[newpos].configure(image=self.bluepix[newpos])
        else:
            self.blist[newpos].configure(image=self.redpix[newpos])
        self.moving = False                                        # both squares of move have been clicked
        if self.boardvalue():                                      # check to see if we won
            self.gameover = True                                   # if so, game is over so we update message
            self.message.configure(text=TMM.messagelist[self.turn])
            return
        self.turn = 3 - self.turn                                  # otherwise it's the other players turn

    def click(self, button):
        if self.gameover:
            return
        x = button.position                                   # number of the button that was clicked
        if self.moving:
            if self.board[x] == 0 and {x,self.savepos} in TMM.edges:
                self.do_move(x, self.savepos, self.turn)      # handles the details of the move
                tmp = player.getmove(self.board, self.turn)   # after we move, the computer moves immediately
                self.do_move(tmp[1], tmp[0], self.turn)
        else:
            if self.board[x] == self.turn:                    # need a reminder of old position
                self.savepos = x
                self.moving = True              

if __name__ == "__main__":

    game = TMM()
    game.mainloop()

