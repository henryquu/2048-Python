import numpy as np
import tkinter as tk
from tkinter.messagebox import showinfo
from itertools import product
from constants import *

class Cell():
    def __init__(self, master, row, column, val=0):
        self.row = row
        self.column = column
        self.master = master
        self.text = None

        self.x = column * (100 + 5) + 12
        self.y = row * (100 + 5) + 12

        y, x = self.y, self.x
        self.id = self.master.create_rectangle(x, y, x + 100, y + 100)

        self.val = val

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
    
        if self.val < 100:
            self.text = self.master.create_text(x, y, text=self.val, font=BIG_FONT)
        elif self.val < 1000:
            self.text = self.master.create_text(x, y, text=self.val, font=SMALL_FONT)
        else:
            val = len(bin(self.val)) - len(bin(self.val).rstrip('0'))
            self.text = self.master.create_text(x, y, text=f"2^{val}", font=SMALL_FONT)

    def update_color(self):
        bg = BACKGROUNDS.get(self.val, "#f67c5f")
        fg = FILL.get(self.val, "#f9f6f2")
        self.master.itemconfig(self.id, fill=bg)
        self.master.itemconfig(self.text, fill=fg)


class Game(tk.Canvas):
    def __init__(self, root, width=4):
        tk.Canvas.__init__(self, root, bg=BG_COLOR)

        self.width= width
        self.cells = np.full((width, width), Cell)
        self.board = np.zeros((width, width), int)
        self.init_cells()

        self.randomly_add_2or4()

        self.set_binds()

    def init_cells(self):
        for y in range(self.width):
            for x in range(self.width):
                self.cells[y][x] = Cell(self, y, x)

    def get_empty(self) -> list:
        cords = product(range(self.width), repeat=2)
        spaces = [(y, x) for y, x in cords if self.board[y][x] == 0]
        return spaces

    def randomly_add_2or4(self):
        spaces = self.get_empty()
        if not spaces:
            return

        i = int(np.random.choice(a = len(spaces)))
        y, x = spaces[i]
        self.board[y][x] = np.random.choice([2, 4], p = [0.9, 0.1])
        self.cells[y][x].val = self.board[y][x]

    def set_binds(self):
        self.bind_all('<KeyRelease>', lambda a: self.input(a.keysym))

    # fixing this function
    def input(self, key):
        if key.lower() not in ['w', 'a', 's', 'd']:
            return False

        # up = transpose  + flip columns + left + transpose
        # down = transpose + right + transpose
        if key in 'WwSs':
            self.board = np.transpose(self.board)
        if key in 'WwAa':
            self.board = np.fliplr(self.board)

        setOfAdded = set() # added numbers can't be added to anything in the same movement
        iter_count = 0
        while self.move_right(setOfAdded):
            iter_count += 1
        
        if key in 'WwAa':
            self.board = np.fliplr(self.board)
        if key in 'WwSs':
            self.board = np.transpose(self.board)

        if not self.get_empty():
            self.result()
    
        if iter_count > 0:
            self.randomly_add_2or4()
            self.refresh_cells()

    def refresh_cells(self):
        for y in range(self.width): 
            for x in range(self.width):
                self.cells[y][x].val = self.board[y][x]

    def move_right(self, added_previously):
        moved = False 

        for y in range(self.width): 
            for x in range(self.width - 1):
                if self.board[y][x] == 0:
                    continue
                if self.board[y][x] == self.board[y][x + 1] and (y, x) not in added_previously:
                    self.board[y][x + 1], self.board[y][x] = self.board[y][x + 1]*2, 0
                    moved = True
                    added_previously.update([(y, x), (y, x + 1)])
                elif self.board[y][x + 1] == 0:
                    self.board[y][x + 1], self.board[y][x] = self.board[y][x], 0
                    if (y, x) in added_previously:
                        added_previously.update((y, x + 1))
                        added_previously.remove((y, x))
                    moved = True

        return moved

    def _print_cells(self):
        for row in self.cells:
            for cell in row:
                print(cell.val, end=' ')
            print()
    
    def result(self):
        max = np.amax(self.board)
        showinfo("Congratulations!", "Your score is " + str(max))

class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("2048")
        
        self.geometry("440x440+500+100")
        self.resizable('no', 'no')

        board = Game(self)
        board.pack(fill="both", expand=True)

        self.mainloop()


if __name__ == "__main__":
    Window()