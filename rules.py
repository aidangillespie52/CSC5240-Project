# rules.py

# imports
from dataclasses import dataclass
from typing import Tuple
import numpy as np
from board import Board
from typing import Optional

@dataclass
class Result:
    idx: Tuple[int, int]
    value: int
    
def single_missing(bd: Board) -> Result:
    """
    Looks for a single missing value within either the row, column or box,
    and returns a result object that has the index
    
    Example:
    12345.789 -> 6 would be the missing in the row
    """
    def check_empty(arr: np.array, x: int) -> Optional[Result]:
        num_missing = bd.count_empty(arr)
        
        if num_missing != 1:
            return None
        
        missing_digit_arr = np.setdiff1d(bd.allowed_values(), arr)
        
        if len(missing_digit_arr) != 1:
            raise ValueError("the board is invalid")
        
        y = int(np.where(arr == 0)[0][0])
        missing_digit = int(missing_digit_arr[0])
        
        return Result((x,y), missing_digit)

    # check rows and cols
    for i in range(bd.size):
        row = bd.get_row(i)
        col = bd.get_col(i)

        # row
        res = check_empty(row, i)
        if res:
            return res
        
        # col
        res = check_empty(col, i)
        if res:
            res.idx = res.idx[::-1]
            return res
    
    for i in range(bd.num_cells):
        cell = bd.get_cell(i)
        res = check_empty(cell, i)
        if not res:
            continue
        
        _, arr_idx = res.idx 
        x,y = bd.cell_index_to_board_index(i, arr_idx)
        res.idx = (x,y)
        return res
    
if __name__ == '__main__':
    print("Test col:")
    b = Board(9,3,3)
    r = np.array(b.allowed_values())
    np.random.shuffle(r)
    
    b[2, :] = r
    np.random.shuffle(r)
    b[:, 5] = r
    b[3,5] = 0
    
    print(b)
    res = single_missing(b)
    print(res)

    print("Test row:")
    b = Board(9,3,3)
    r = np.array(b.allowed_values())
    np.random.shuffle(r)
    
    b[3, :] = r
    np.random.shuffle(r)
    b[5, :] = r
    b[5,3] = 0
    
    print(b)
    res = single_missing(b)
    print(res)

    print("Test cell:")
    b = Board(9,3,3)
    b[3,0] = 9
    b[3,1] = 5
    b[3,2] = 3
    b[4,0] = 1
    b[4,1] = 4
    b[4,2] = 6
    b[5,0] = 7
    b[5,1] = 8
    b[5,2] = 0

    print(b)
    res = single_missing(b)
    print(res)

