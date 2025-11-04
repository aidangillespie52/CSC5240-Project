# system prompt
SYS_PROMPT = \
"""
You are a helpful agent that is an amazing sudoku tutor.
You will give clear and concise answers, and you will think
step by step.
"""

def build_hint_query(board) -> str:
    return (
        "Make sure to use 1 based indexing."
        "This is the current sudoku board:\n"
        f"{board}\n"
        "Give a hint with short amount of reasoning."
        "If you display a row or column on the board "
        "make sure that you wrap it with %%."
    )

def build_highlight_query(hint_text: str) -> str:
    return (
        "Make sure to use 1 based indexing."
        "Find the board position and value that the hint is talking about and "
        "return only respond with (x,y,z) where x is x, y is y, and z is value.\n"
        f"Hint:\n{hint_text}"
    )