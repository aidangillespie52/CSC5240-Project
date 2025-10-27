# board.py

# imports
import numpy as np
import random

class Board:
    def __init__(self, size: int, box_cols: int, box_rows: int, fill=0):
        self._validate_init(size, box_rows, box_cols)
        
        self.size = size
        self.box_cols = box_cols
        self.box_rows = box_rows
        self.fill = fill
        self._grid = np.full((size, size), fill, dtype=int)

    @staticmethod
    def _validate_init(size, box_rows, box_cols):
        # make sure its an actual board size
        if size <= 0:
            raise ValueError("size must be a positive integers")
        
        # ensure that boxes are proper
        if size % box_rows != 0:
            raise ValueError(f"size ({size}) must be divisible by box_rows ({box_rows})")
        if size % box_cols != 0:
            raise ValueError(f"size ({size}) must be divisible by box_cols ({box_cols})")

    def __getitem__(self, idx):
        return self._grid[idx]

    def __setitem__(self, idx, value):
        self._grid[idx] = value

    def __iter__(self):
        return iter(self._grid)

    def __str__(self):
        lines = []
        for r, row in enumerate(self._grid):
            # replace 0's with "."
            line = " ".join("." if v == 0 else str(v) for v in row)

            # vertical dividers
            parts = []
            for i in range(0, self.size, self.box_cols):
                parts.append(" ".join("." if v == 0 else str(v) for v in row[i:i+self.box_cols]))
            line = " | ".join(parts)

            lines.append(line)

            # horizontal dividers
            if (r + 1) % self.box_rows == 0 and (r + 1) < self.size:
                lines.append("-" * (self.size * 2 + (self.size // self.box_cols - 1) * 2))
        
        return "\n".join(lines)

    def __repr__(self):
        return self.__str__()

    def reset(self):
        self._grid.fill(self.fill)

    # just for testing purposes
    def random(self, no_empty=False):
        lower_bound = 0
        if no_empty:
            lower_bound = 1
            
        self._grid = np.random.randint(lower_bound, self.size, size=(self.size, self.size))
        
    # helper methods for rules logic
    def count_row(self, y, x):
        val = self._grid[y, x]
        return np.count_nonzero(self._grid[y, :] == val)

    def count_col(self, y, x):
        val = self._grid[y, x]
        return np.count_nonzero(self._grid[:, x] == val)

    def count_box(self, y, x):
        val = self._grid[y, x]
        
        box_y = (y // self.box_rows) * self.box_rows
        box_x = (x // self.box_cols) * self.box_cols
        box = self._grid[box_y:box_y+self.box_rows, box_x:box_x+self.box_cols]
        
        return np.count_nonzero(box == val)

    def is_valid(self):
        # check rows
        for y in range(self.size):
            row = self.get_row(y)
            filtered_row = row[row != 0]
            
            if len(set(filtered_row)) != len(filtered_row):
                return False
        
        # check cols
        for x in range(self.size):
            col = self.get_col(x)
            filtered_col = col[col != 0]
            
            if len(set(filtered_col)) != len(filtered_col):
                return False
        
        # TODO: check boxes
        
        return True
    
    def count_empty(self):  return np.count_nonzero(self._grid == 0)
    def count_empty_row(self, y: int) -> int:   return np.count_nonzero(self._grid[y, :] == 0)
    def count_empty_col(self, x: int) -> int:   return np.count_nonzero(self._grid[:, x] == 0)
    def get_row(self, y: int):  return self._grid[y, :]
    def get_col(self, x: int):  return self._grid[:, x]
    def allowed_values(self):   return np.array(range(1, self.size + 1))

if __name__ == '__main__':
    b = Board(9, 3, 3)
    b.random()
    print(b)
    print("valid:", b.is_valid())
    
    b = Board(9,3,3)
    r = np.array(b.allowed_values())
    np.random.shuffle(r)    
    b[2, :] = r
    b[2,5] = 0

    print(b)
    print("valid:", b.is_valid())