# Updated 10 April 2024

import tkinter as tk
from tkinter import scrolledtext, ttk
from game import MinesweeperInstance
import datetime
import time
from pathlib import Path

class Minesweeper(tk.Tk):
    """
    Minesweeper game
    """
    def __init__(self):
        super().__init__()
        self.title("Minesweeper")
        self.maxsize(1920, 1080)
        self.running_switch = tk.BooleanVar()
        self.running_switch.set(True)
        self.time_var = tk.StringVar()
        self.time_var.set("0:00:00")
        self.bomb_var = tk.StringVar()

        self.bind("<Key>", self._key_press)

        self._draw()
        self.running = self.after(1000, self.update)
        self.insert_records()

    def _key_press(self, event):
        if (event.char == " "):
            self.new_game()
        else:
            self.game._key_press(event)

    def _draw(self):
        """
        Creates and places widgets
        """
        self.game_frame = tk.Frame(self)
        self.game_frame.pack(side = "left", expand = True, padx = 5, pady = 5, fill = "both")
        side_frame = tk.Frame(self)
        side_frame.pack(side = "right", expand = True)

        header = tk.Label(side_frame, text = "Minesweeper", font = ("", 16))
        header.pack(side = "top")

        time_label = tk.Label(side_frame, textvariable = self.time_var, font = ("", 12))
        time_label.pack(pady = 10)

        new_game_frame = tk.Frame(side_frame)
        new_game_frame.pack(fill = "both", expand = True, padx = 20, pady = 10)
        new_game_button = tk.Button(new_game_frame, text = "New Game", command = self.new_game, font = ("", 12))
        new_game_button.pack(side = "left")
        self.dimension_choice = ttk.Combobox(new_game_frame, values = [str(i) for i in range(4, 21)], state = "readonly")
        self.dimension_choice.pack(side = "right")
        self.dimension_choice.current(4)

        self.game = MinesweeperInstance(self.game_frame, dimension = int(self.dimension_choice.get()), switch = self.running_switch)
        self.game.pack()

        self.bomb_var.set(f"Bombs Remaining: {self.game.bomb_remaining} / {self.game.bomb_count}")
        bomb_count_label = tk.Label(side_frame, textvariable = self.bomb_var, font = ("", 12))
        bomb_count_label.pack(pady = 10)

        self.record_panel = scrolledtext.ScrolledText(side_frame, width = 35, height = 11)
        self.record_panel.pack(pady = 10)

    def play(self):
        """
        Starts the game
        """
        self.start = time.time()
        self.mainloop()

    def insert_records(self):
        """
        Clears records panel and inserts records from file
        """
        self.record_panel.config(state = "normal")
        self.record_panel.delete("1.0", "end")
        file = Path(__file__).parent.resolve() / "records.txt"
        with open(file, "r") as f:
            records = sorted([line.strip().split(",") for line in f.readlines()], key = lambda x: float(x[2]))
            records = [f"{i[0][:6]:7}| {i[1]} | {f'{int((float(i[2])%3600)//60):02d}:{int(float(i[2])%60):02d}'}" for i in records if int(i[3]) == self.game.dimension]
        self.record_panel.insert("insert", "\n".join([f"{n + 1:3}| {i}" for n,i in enumerate(records[:10])]))
        self.record_panel.config(state = "disabled")

    def update(self):
        """
        Updates timer and bomb count
        """
        self.time_var.set(str(datetime.timedelta(seconds = int(time.time() - self.start))))
        self.bomb_var.set(f"Bombs Remaining: {self.game.bomb_remaining} / {self.game.bomb_count}")
        self.running = self.after(1000, self.update)
        if not self.running_switch.get():
            self.after_cancel(self.running)

    def new_game(self):
        """
        Starts a new game
        """
        for child in self.game_frame.winfo_children():
            child.destroy()
        self.game = MinesweeperInstance(self.game_frame, dimension = int(self.dimension_choice.get()), switch = self.running_switch)
        self.game.pack()
        self.running_switch.set(True)
        self.running = self.after(1000, self.update)
        self.insert_records()
        self.game_frame.focus_force()
        self.start = time.time()

if __name__ == "__main__":
    game = Minesweeper()