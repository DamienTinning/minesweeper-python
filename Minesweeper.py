import random
import tkinter as tk
from tkinter import messagebox

# size of map and number of squares

SIZE = 8
MINES = 10
CELL_SIZE = 40

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")

        self.buttons = []
        self.mines = set()
        self.revealed = set()

        self.create_board()
        self.place_mines()

    def create_board(self):
        for r in range(SIZE):
            row = []
            for c in range(SIZE):
                btn = tk.Button(
                    self.root,
                    width=3,
                    height=1,
                    command=lambda r=r, c=c: self.click(r, c)
                )
                btn.grid(row=r, column=c)
                row.append(btn)
            self.buttons.append(row)

    def place_mines(self):
        while len(self.mines) < MINES:
            r = random.randint(0, SIZE-1)
            c = random.randint(0, SIZE-1)
            self.mines.add((r, c))

    def count_adjacent(self, r, c):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (r+i, c+j) in self.mines:
                    count += 1
        return count

# this is how squares are revealed

    def reveal(self, r, c):
        if (r, c) in self.revealed:
            return

        self.revealed.add((r, c))

        if (r, c) in self.mines:
            self.buttons[r][c].config(text="💣", bg="red")
            self.game_over(False)
            return

# this is how the system reads the number of mines next to the boarder squares

        count = self.count_adjacent(r, c)
        self.buttons[r][c].config(text=str(count) if count > 0 else "", relief=tk.SUNKEN)

        if count == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    nr, nc = r+i, c+j
                    if 0 <= nr < SIZE and 0 <= nc < SIZE:
                        self.reveal(nr, nc)

        if len(self.revealed) == SIZE*SIZE - MINES:
            self.game_over(True)

    def click(self, r, c):
        self.reveal(r, c)

    def game_over(self, win):
        for r, c in self.mines:
            self.buttons[r][c].config(text="💣")

        if win:
            messagebox.showinfo("Game Over", "You Win!")
        else:
            messagebox.showinfo("Game Over", "You hit a mine!")

        self.root.destroy()


root = tk.Tk()
game = Minesweeper(root)
root.mainloop()
