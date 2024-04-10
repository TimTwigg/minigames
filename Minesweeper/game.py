# Updated 10 April 2024

import tkinter as tk
from tkinter import simpledialog
import math
import random
import time
from pathlib import Path

class Square(tk.Frame):
    """
    Square object, subclass of tkinter.Frame

    Represents a single cell in the Minesweeper
    """
    def __init__(self, parent, x:int, y:int):
        """
        params:
            parent::Minesweeper object, passed to tk.Frame.__init__ as root
            x::int, x coordinate of cell in parent grid
            y::int, y coordinate of cell in parent grid
        """
        super().__init__(parent, borderwidth = 1, relief = "solid", height = 40, width = 100)
        self.ms = parent
        self.cell_type = "clear"
        self.number = tk.IntVar()
        self.number.set(0)
        self.button = tk.Button(self, relief = "flat", bg = "gray70", font = ("", 16), activebackground = "gray70")
        self.button.pack(fill = "both", expand = True)
        self.label = tk.Label(self, font = ("", 16))
        self.id = (x, y)
        self.active = False

        self.button.bind("<Button>", self._button_press)

    def _button_press(self, event):
        if event.num == 1:
            self._activate()
        elif event.num == 2 or event.num == 3:
            self.button.config(text = "X" if self.button.cget("text") == "" else "")
        self.ms.test_complete()
        self.ms._count_bombs_remaining()

    def _activate(self):
        """
        Internal function called by clicking the button. Reveals the number or bomb
        """
        if self.cell_type == "bomb":
            self.ms.lose_game()
        elif self.cell_type == "clear":
            self.set()
            self.active = True
            self.button.config(text = "")
            # self.ms.reveal is called multiple times to loop over the revealing algorithm multiple times
            # required to properly execute reveal
            for _ in range(math.ceil(math.sqrt(self.ms.dimension))):
                self.ms.reveal()

    def set(self):
        """
        Setup method to set label number and color
        """
        self.button.pack_forget()
        colors = ["black", "blue", "green", "red", "purple", "black"]
        self.label.config(text = self.number.get() if self.number.get() > 0 else "", fg = colors[self.number.get()], bg = "white")
        self.label.pack(fill = "both", expand = True)

    def bombify(self):
        """
        Comvert Square to bomb cell
        """
        self.cell_type = "bomb"

    def __str__(self):
        """
        Defines how to be represented as a string
        """
        d = {
            "id": self.id,
            "cell_type": self.cell_type,
            "number": self.number,
            "active": self.active
        }
        return str(d)


class MinesweeperInstance(tk.LabelFrame):
    """
    Minesweeper object, subclass of tk.LabelFrame

    The main game, requires a tk.Tk root
    """
    record_file = Path(__file__).parent.resolve() / "records.txt"
    def __init__(self, root:tk.Tk, dimension:int = 8, switch:tk.BooleanVar = None):
        """
        root::tk.Tk root
        dimension::int, width and height for game. Default value: 8
        """
        super().__init__(root, text = "Minesweeper", borderwidth = 3, labelanchor = "n")
        self.root = root
        self.widgets = []
        self.dimension = dimension
        self.bomb_count = int(math.sqrt(1.5**dimension) + (5 if dimension > 6 else math.ceil(dimension / 2)))
        self.bomb_remaining = self.bomb_count
        self.bombs = []
        self.switch = switch

        for i in range(self.dimension):
            self.grid_columnconfigure(i, minsize = 40)
            self.grid_rowconfigure(i, minsize = 40)
        
        for x in range(dimension):
            col = []
            for y in range(dimension):
                cell = Square(self, x, y)
                col.append(cell)
                cell.grid(row = y, column = x, sticky = "nesw")
            self.widgets.append(col)

        self._place_bombs()
        self._count_bombs()
        if not self.record_file.exists():
            self.record_file.touch()
        self.start = time.time()

    def _key_press(self, event):
        b = self.winfo_containing(event.x_root, event.y_root)
        if (type(b) != tk.Button):
            return
        if event.char == "x":
            b.config(text = "X" if b.cget("text") == "" else "")
            self.test_complete()
            self._count_bombs_remaining()
        elif event.char == "z":
            b.master._activate()

    def _place_bombs(self):
        """
        Convert cells selected at random to bombs
        """
        i = 0
        while i < self.bomb_count:
            x = random.randint(0,self.dimension - 1)
            y = random.randint(0,self.dimension - 1)
            cell = self.widgets[x][y]
            if cell.cell_type == "bomb":
                continue
            cell.bombify()
            self.bombs.append((x,y))
            i += 1

    def _count_bombs(self):
        """
        Update cells to show number of neighbouring bombs
        """
        for (x,y) in self.bombs:
            for cell in self.neighbours(x, y):
                    if cell.cell_type != "bomb":
                        cell.number.set(cell.number.get() + 1)

    def _count_bombs_remaining(self):
        """
        Count how many cells have been marked as bombs, subtract from total bomb count
        """
        n = sum([1 for cell in self if cell.button.cget("text") == "X"])
        self.bomb_remaining = self.bomb_count - n

    def __iter__(self):
        l = []
        for i in self.widgets:
            l += i
        return (i for i in l)

    def neighbours(self, x, y):
        """
        Generator iterator to iterate through a cell's neighbours. Cell defined by x and y coordinates in parameter
        """
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):

                if i == x and j == y:
                    continue
                if (0 <= i < self.dimension) and (0 <= j < self.dimension):
                    yield self.widgets[i][j]

    def border_clear(self, x, y):
        """
        Returns True if the cell borders a visible neighbour which is clear and 0
        """
        for cell in self.neighbours(x, y):
            if cell.cell_type == "clear" and cell.active is True and cell.number.get() == 0:
                return True
        return False

    def reveal(self):
        """
        Reveals empty cells around clicked cell
        """
        for cell in self:
            if cell.cell_type == "clear" and self.border_clear(*cell.id):
                cell.set()
                cell.active = True

    def test_complete(self):
        """
        Checks if all bombs have been located and the game won
        """
        clear_complete = True
        bombs_complete = True
        clear_incorrect = False
        for cell in self:
            if cell.cell_type == "clear" and not cell.active:
                clear_complete = False
                if cell.button.cget("text") == "X":
                    clear_incorrect = True
                    break
            elif cell.cell_type == "bomb" and cell.button.cget("text") == "":
                bombs_complete = False
        if (clear_complete or bombs_complete) and not clear_incorrect:
            self.win_game()

    def end_game(self):
        end = time.time()
        for cell in self:
            cell.button.unbind("<Button>")
        gametime = end - self.start
        if self.switch is not None:
            self.switch.set(False)
        return gametime

    def lose_game(self):
        for (x,y) in self.bombs:
            cell = self.widgets[x][y]
            cell.button.pack_forget()
            cell.label.config(bg = "red4")
            cell.label.pack(fill = "both", expand = True)
        self.end_game()

    def win_game(self):
        gametime = self.end_game()
        date = time.strftime("%d-%m-%Y", time.gmtime())
        name = simpledialog.askstring("Name", "Congratulations! You Won!\n  Enter Name:")
        with open(self.record_file, "a") as f:
            f.write(f"{name},{date},{gametime},{self.dimension}\n")