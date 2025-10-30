# board.py

import numpy as np

def read_sudoku(filepath):
    board = []
    
    with open(filepath, "r") as f:
        for line in f.readlines():
            row = []
            s = line.strip()
            
            for x in s:
                row.append(int(x))

            board.append(row)
    
    return np.array(board)