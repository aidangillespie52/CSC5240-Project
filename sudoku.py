# defaults (clear, discoverable)
DEFAULT_ROWS = 9
DEFAULT_COLS = 9
DEFAULT_BOX_COLS = 3
DEFAULT_BOX_ROWS = 3

class Sudoku:
    def __init__(self):
        self._board = [[0 for _ in range(DEFAULT_COLS)] for _ in range(DEFAULT_ROWS)]
    
    def __str__(self):
        str_board = [["." if x == 0 else x for x in row] for row in self._board]
        return "\n".join(" ".join(map(str, row)) for row in str_board)
    
    def populate(self):
        pass

s = Sudoku()
print(str(s))