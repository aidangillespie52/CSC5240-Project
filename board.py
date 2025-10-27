class Board:
    def __init__(self, rows: int, cols: int, box_cols: int, box_rows: int, fill=0):
        self._grid = [[fill] * cols for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        self.box_cols = box_cols
        self.box_rows = box_rows

    def __getitem__(self, idx):
        return self._grid[idx]

    def __setitem__(self, idx, value):
        self._grid[idx] = value

    def __iter__(self):
        return iter(self._grid)

    def __str__(self):
        return "\n".join(" ".join(map(str, row)) for row in self._grid)

    def count_row(self, qy, qx):
        val = self._grid[qy][qx]
        
        c = 0

        for y in range(self.cols):
            v = self._grid[y][qx]
            if v == val:
                c += 1
        
        return c
    
    def count_col(self, qy, qx):
        val = self._grid[qy][qx]
        
        c = 0

        for x in range(self.rows):
            v = self._grid[qy][x]
            if v == val:
                c += 1
        
        return c

    # TODO: finish implementing this
    #def count_box(self, y, x):
    #    pass

    def count_empty(self):
        return sum(cell == 0 for row in self._grid for cell in row)

b = Board(9, 9, )
print(str(b))