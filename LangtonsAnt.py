#!/usr/bin/env python

import Tkinter as tk

BOARD_SIZE = 100 # i.e. 50x50 cell grid
delay = 1 # (milliseconds)

class App(tk.Tk):
    
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.wm_title("Langton's Ant")
        self.resizable(width=False, height = False)

        self.cellwidth = 5
        self.cellheight = 5
        
        # Length of side of window (px)
        self.size = (BOARD_SIZE * self.cellwidth) 
        
        self.canvas = tk.Canvas(self, width=self.size, 
                                height=self.size, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
            
        self.rect = {}

        for column in xrange(self.size/self.cellwidth):
            for row in xrange(self.size/self.cellheight):
                
                x1 = column*self.cellwidth
                y1 = row*self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight

                self.rect[row, column] = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="white", tags="rect")

        # Array to keep track of desired colour for each cell:
        self.colourArray = [[0 for x in xrange(BOARD_SIZE)] 
                            for y in xrange(BOARD_SIZE)] 

        # Create new active square (the 'Ant'):
        self.active = ActiveSquare()

        self.colourArray[self.active.currX][self.active.currY] = 1

        self.updateColours(iCount = 0)


    def updateColours(self, iCount):

        """
        Updates colourArray with the correct colour for the next screen 
        refresh.
        """
        
        # Remember, in the context of colourArray: 0 == white; 1 == black

        if self.colourArray[self.active.currX][self.active.currY] == 0:
            self.colourArray[self.active.currX][self.active.currY] = 1
            self.canvas.itemconfig(
                self.rect[self.active.currY, self.active.currX],fill="black")
            self.active = self.active.rotateRight()

        else:
            self.colourArray[self.active.currX][self.active.currY] = 0
            self.canvas.itemconfig(
                self.rect[self.active.currY, self.active.currX],fill="white")
            self.active = self.active.rotateLeft()

        self.active = self.active.moveOne()

        self.canvas.itemconfig(
            self.rect[self.active.currY,self.active.currX],fill="red")

        if iCount % 100 == 0: print iCount

        self.after(delay, lambda: self.updateColours(iCount+1))


class ActiveSquare:

    """
    Class to represent the red, active, square. The is the 'Ant'.
    """

    def __init__(self, currX = BOARD_SIZE/2, currY = BOARD_SIZE/2, 
                    direction = 'U'):
        self.currX = currX
        self.currY = currY
        self.direction = direction

    def rotateRight(self):

        if self.direction == 'U': self.direction = 'R'
        elif self.direction == 'R': self.direction = 'D'
        elif self.direction == 'D': self.direction = 'L'
        elif self.direction == 'L': self.direction = 'U'

        return self

    def rotateLeft(self):
        
        if self.direction == 'U': self.direction = 'L'
        elif self.direction == 'R': self.direction = 'U'
        elif self.direction == 'D': self.direction = 'R'
        elif self.direction == 'L': self.direction = 'D'

        return self

    def moveOne(self):

        if self.direction == 'U': self.currY -= 1
        if self.direction == 'D': self.currY += 1
        if self.direction == 'L': self.currX -= 1
        if self.direction == 'R': self.currX += 1

        return self

        
if __name__ == "__main__":
    
    app = App()
    app.mainloop()