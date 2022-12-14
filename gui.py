import numpy as np
import tkinter as tk
from itertools import product
from constants import *

class Cell():
    font = ('Helvetica','30','bold')

    def __init__(self, master, row, column):
        self.row = row
        self.column = column
        self.master = master
        self.text = None

        self.x = column * (100 + 5) + 12
        self.y = row * (100 + 5) + 12

        self.val = 0

        y, x = self.y, self.x
        self.master.create_rectangle(x, y, x + 100, y + 100)
        self.update_color()

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, new_val):
        self._val = new_val
        self.update_text()
        self.update_color()

    def update_text(self):
        if self.text:
            self.master.delete(self.text)
        y, x = self.y + 50, self.x + 50
        self.text = self.master.create_text(x, y, text=self.val, font=Cell.font)

    def update_color(self):
        self.master.itemconfig(self, fill=BACKGROUNDS[self.val])


class Board(tk.Canvas):
    def __init__(self, root, width=4):
        tk.Canvas.__init__(self, root, bg=BG_COLOR)

        self.width= width

        self.cells = np.full((width, width), Cell)
        self.init_cells()
        self.randomly_add_2or4()

        self.set_binds()


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
            self.cells[y][x].val = np.random.choice([2, 4], p = [0.9, 0.1])
            return True
        else:
            print('Game Over!')
            return False

    def set_binds(self):
        self.bind_all('<KeyRelease>', lambda a: self.move(a.keysym))

    # fixing this function
    def move(self, key):
        if key.lower() not in ['w', 'a', 's', 'd']:
            return False

        # down = transpose + right + transpose
        # up = transpose  + left + transpose
        if key in 'WwSs':
            np.transpose(self.cells)
        if key in 'WwAa':
            np.fliplr(self.cells)

        setOfAdded = set() # added numbers can't be added to anything else in the same movement
        while True:
            moved = False # check if board changed in this set of iterations, if not -> break loop
            for y in range(self.width): 
                for x in range(self.width - 1):
                    if self.cells[y][x].val != 0:
                        if self.cells[y][x].val == self.cells[y][x + 1].val and ((y, x) or (y, x + 1)) not in setOfAdded:
                            self.cells[y][x + 1].val, self.cells[y][x].val = self.cells[y][x + 1].val*2, 0
                            moved = True
                            setOfAdded.update([(y, x), (y, x + 1)])
                        elif self.cells[y][x + 1].val == 0:
                            self.cells[y][x + 1].val, self.cells[y][x].val = self.cells[y][x].val, 0
                            moved = True
                            if (y, x) in setOfAdded:
                                setOfAdded.add((y, x + 1))
            if not moved:
                break   

        if key in 'WwAa':
            np.fliplr(self.cells)
        if key in 'WwSs':
            np.transpose(self.cells)

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