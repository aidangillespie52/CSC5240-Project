# rules.py

# imports
from dataclasses import dataclass
from typing import Tuple
import numpy as np
from board import Board

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
    
    # check the rows
    for y in range(bd.size):
        num_missing = bd.count_empty_row(y)
        
        if num_missing != 1:
            continue
        
        row = bd.get_row(y)
        missing_digit_arr = np.setdiff1d(bd.allowed_values(), row)
        
        if len(missing_digit_arr) != 1:
            raise ValueError("the board is invalid")
        
        x = int(np.where(row == 0)[0][0])
        missing_digit = int(missing_digit_arr[0])
        
        return Result((x,y), missing_digit)
    
    # check the cols
    for x in range(bd.size):
        num_missing = bd.count_empty_col(x)
        
        if num_missing != 1:
            continue
        
        col = bd.get_col(x)
        print(col)
        
        missing_digit_arr = np.setdiff1d(bd.allowed_values(), col)
        
        if len(missing_digit_arr) != 1:
            raise ValueError("the board is invalid")
        
        y = int(np.where(col == 0)[0][0])
        missing_digit = int(missing_digit_arr[0])
        
        return Result((x,y), missing_digit)
    
    # check the boxes
    # TODO: implement the checking the boxes for single digits missing
    
if __name__ == '__main__':
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