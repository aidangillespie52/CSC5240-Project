import os
import asyncio
from typing import Tuple
import re

import aiohttp
from dotenv import load_dotenv

from board import Board
from queries import build_highlight_query, build_hint_query, SYS_PROMPT
from rules import solve

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
URL = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}
MODEL = "gpt-4o-mini"

async def chat_once(session: aiohttp.ClientSession, user_content: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYS_PROMPT},
            {"role": "user", "content": user_content},
        ]
    }
    async with session.post(URL, headers=HEADERS, json=payload, timeout=60) as resp:
        if resp.status != 200:
            raise RuntimeError(f"LLM error {resp.status}: {await resp.text()}")
        data = await resp.json()
        return data["choices"][0]["message"]["content"]
    
async def get_hint(session: aiohttp.ClientSession, board) -> str:
    """
    Returns a short hint (with brief reasoning) for the given board.
    """
    return await chat_once(session, build_hint_query(board))

async def get_highlight_location(session: aiohttp.ClientSession, hint_text: str) -> Tuple[int, int]:
    """
    Returns (x, y) parsed from the LLM response, e.g., '(3,5)' -> (3, 5).
    Raises ValueError if not found.
    """
    raw = await chat_once(session, build_highlight_query(hint_text))
    m = re.search(r"\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", raw)
    if not m:
        raise ValueError(f"Could not parse coordinates from: {raw!r}")
    return int(m.group(1)), int(m.group(2)), int(m.group(3))

async def _demo():
    b = Board(9,3,3)
    t = Board(9,3,3)
    
    b.read_file("sample.txt")
    t.read_file("sample.txt")
    
    print(b)
    solve(b)
    
    async with aiohttp.ClientSession() as session:
        hint = await get_hint(session, str(t))
        print("HINT:\n", hint)
        xyz = await get_highlight_location(session, hint)
        t[xyz[0]-1, xyz[1]-1] = xyz[2]
        print("new board:\n", t, "\n")

if __name__ == "__main__":
    asyncio.run(_demo())