import tkinter as tk
import random


class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.root.attributes('-topmost', True)
        self.size = 4
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.cells = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                label = tk.Label(self.frame, text='', width=4, height=2, font=('Arial', 24, 'bold'), bg='lightgray',
                                 relief='ridge')
                label.grid(row=i, column=j, padx=5, pady=5)
                row.append(label)
            self.cells.append(row)

        self.spawn_tile()
        self.spawn_tile()
        self.update_grid()

        self.root.bind("<KeyPress>", self.handle_keypress)

    def spawn_tile(self):
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def update_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                value = self.grid[i][j]
                self.cells[i][j].config(text=str(value) if value else '', bg=self.get_color(value))

    def get_color(self, value):
        colors = {
            0: 'lightgray', 2: 'lightyellow', 4: 'khaki', 8: 'orange', 16: 'darkorange',
            32: 'red', 64: 'darkred', 128: 'purple', 256: 'blue', 512: 'navy',
            1024: 'green', 2048: 'gold'
        }
        return colors.get(value, 'black')

    def handle_keypress(self, event):
        if event.keysym in ('Up', 'Down', 'Left', 'Right'):
            self.move(event.keysym)

    def move(self, direction):
        rotated = False
        if direction == 'Up':
            self.grid = self.transpose(self.grid)
        elif direction == 'Down':
            self.grid = self.transpose(self.grid[::-1])
        elif direction == 'Right':
            self.grid = [row[::-1] for row in self.grid]

        moved = self.merge()

        if direction == 'Up':
            self.grid = self.transpose(self.grid)
        elif direction == 'Down':
            self.grid = self.transpose(self.grid)[::-1]
        elif direction == 'Right':
            self.grid = [row[::-1] for row in self.grid]

        if moved:
            self.spawn_tile()
            self.update_grid()
            if self.check_game_over():
                self.game_over()

    def merge(self):
        moved = False
        for row in self.grid:
            filtered = [num for num in row if num != 0]
            merged = []
            skip = False
            for i in range(len(filtered)):
                if skip:
                    skip = False
                    continue
                if i < len(filtered) - 1 and filtered[i] == filtered[i + 1]:
                    merged.append(filtered[i] * 2)
                    self.score += filtered[i] * 2
                    skip = True
                    moved = True
                else:
                    merged.append(filtered[i])
            merged.extend([0] * (self.size - len(merged)))
            if row != merged:
                moved = True
            row[:] = merged
        return moved

    def transpose(self, grid):
        return [list(row) for row in zip(*grid)]

    def check_game_over(self):
        for row in self.grid:
            if 0 in row:
                return False
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.grid[i][j] == self.grid[i][j + 1] or self.grid[j][i] == self.grid[j + 1][i]:
                    return False
        return True

    def game_over(self):
        game_over_label = tk.Label(self.root, text="Game Over!", font=('Arial', 24, 'bold'), fg='red')
        game_over_label.pack()
        self.root.unbind("<KeyPress>")


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
