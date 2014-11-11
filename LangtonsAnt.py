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

        self.counter = tk.Label(self, text = "Steps moved: 0")
        self.counter.pack()

        userString = raw_input("Enter the desired sequence: ")

        # Dictinary format: a:[b,c] means: if current direction == a, then
        # rotate according to b, and change current square's colour to c 

        #'RR' == 'rotate right'; 'RL' == 'rotate left'

        self.rulesDict = {}

        for i in xrange(0,len(userString)):
            if userString[i] == 'R':
                self.rulesDict[i] = ['RR', i+1]
            else:
                self.rulesDict[i] = ['RL', i+1]

        self.rulesDict[len(self.rulesDict)-1][1] = 0

        self.colourDict = {
            0: 'dodger blue', 
            1: 'green', 
            2: 'red', 
            3: 'yellow',
            4: 'orange',
            5: 'seagreen1',
            6: 'sienna1',
            7: 'purple2',
            8: 'cyan',
            9: 'green4',
            10: 'blue2'
            }


        self.updateColours(iCount = 0)


    def updateColours(self, iCount):

        """
        Updates colourArray with the correct colour for the next screen 
        refresh.
        """

        self.counter.configure(text = "Steps moved: " + str(iCount))

        currentColour = self.colourArray[self.active.currX][self.active.currY]

        if self.rulesDict[currentColour][0] == 'RR':
            self.active = self.active.rotateRight()

        else:
            self.active = self.active.rotateLeft()

        self.colourArray[self.active.currX][self.active.currY] = self.rulesDict[currentColour][1]
        currentColour = self.colourArray[self.active.currX][self.active.currY]

        self.canvas.itemconfig(
                self.rect[self.active.currY, self.active.currX],
                fill=self.colourDict[currentColour])



        self.active = self.active.moveOne()

        self.canvas.itemconfig(
            self.rect[self.active.currY,self.active.currX],fill="black")

        self.after(delay, lambda: self.updateColours(iCount+1))


class ActiveSquare:

    """
    Class to represent the black, active, square. The is the 'Ant'.
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