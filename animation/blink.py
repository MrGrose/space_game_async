import curses

from utils import sleep


async def blink(canvas, row, column, symbol, offset_tics):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(offset_tics)

        canvas.addstr(row, column, symbol)
        await sleep(offset_tics)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(offset_tics)

        canvas.addstr(row, column, symbol)
        await sleep(offset_tics)