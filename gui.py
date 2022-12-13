import numpy as np
import tkinter as tk
from itertools import product
from constants import *

class Cell():
    def __init__(self, master, row, column):
        self.row = row
        self.column = column
        self.master = master
        self._val = 0

        self.x = column * (100 + 5) + 12
        self.y = row * (100 + 5) + 12

        y, x = self.y, self.x
        self.master.create_rectangle(x, y, x + 100, y + 100)
        self.update_color()

    @property
    def val(self):
        return self._val

    @val.setter
    def set_val(self, new_val):
        self._val = new_val
        self.update_text()

    def update_text(self):
        y, x = self.y + 50, self.x + 50
        self.master.create_text(x, y, text=self.val)
        self.update_color()

    def update_color(self):
        self.master.itemconfig(self, fill=BACKGROUNDS[self.val])

class Board(tk.Canvas):
    def __init__(self, root, width=4):
        tk.Canvas.__init__(self, root, bg=BG_COLOR)
        self.width= width
        self.cells = np.full((width, width), Cell)
        self.init_cells()
        self.randomly_add_2or4()

    def init_cells(self):
        for y in range(self.width):
            for x in range(self.width):
                self.cells[y][x] = Cell(self, y, x)

    def get_empty(self) -> list:
        cords = product(range(self.width), repeat=2)
        spaces = [(y, x) for y, x in cords if self.cells[y][x].val == 0]
        return spaces

    def randomly_add_2or4(self):
        spaces = self.get_empty()
        if spaces:
            i = int(np.random.choice(a = len(spaces)))
            y, x = spaces[i]
            self.cells[y][x]= np.random.choice([2, 4], p = [0.9, 0.1])
            return True
        else:
            print('Game Over!')
            return False


    # not done yet
    def transpose(self):
        for y in range(self.width):
            for x in range(y):
                self.cells[y][x], self.cells[x][y] = self.cells[x][y], self.cells[y][x] 
    
    def reverse_columns(self):
        for column in self.cells:
            column.reverse()

    def move(self):
        while (key := input("Input: ")).lower() not in ['w', 'a', 's', 'd']:
            pass

        # down = transpose + right + transpose
        # up = transpose  + left + transpose
        if key in 'WwSs':
            self.transpose()
        if key in 'WwAa':
            self.reverse_columns()

        repeatIfNotMoved = True # check whether board moved at all, if not -> repeat whole function
        setOfAdded = set() # added numbers can't be added to anything else in the same movement
        while True:
            moved = False # check if board changed in this set of iterations, if not -> break loop
            for y in range(self.width): 
                for x in range(self.width - 1):
                    if self.board[y][x] != 0:
                        if self.cells[y][x] == self.cells[y][x + 1] and ((y, x) or (y, x + 1)) not in setOfAdded:
                            self.cells[y][x + 1], self.cells[y][x] = self.cells[y][x + 1]*2, 0
                            moved = True
                            setOfAdded.update([(y, x), (y, x + 1)])
                        elif self.cells[y][x + 1] == 0:
                            self.cells[y][x + 1], self.cells[y][x] = self.cells[y][x], 0
                            moved = True
                            if (y, x) in setOfAdded:
                                setOfAdded.add((y, x + 1))
            if not moved:
                break   
            else: 
                repeatIfNotMoved = False

        if key in 'WwAa':
            self.reverse_columns()
        if key in 'WwSs':
            self.transpose()
        if repeatIfNotMoved:
            self.move()


class Game(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("2048")
        
        self.geometry("440x440+500+100")
        self.resizable('no', 'no')

        board = Board(self)
        board.pack(fill="both", expand=True)

        self.mainloop()

if __name__ == "__main__":
    Game()