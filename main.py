import curses
import random
import time

from animation.blink import blink
from animation.fire import fire
from animation.spaceship import animate_spaceship
from utils import get_rocket_frame

TIC_TIMEOUT = 0.1


def main(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.border()
    height, width = canvas.getmaxyx()
    canvas.addstr(0, 0, f"Height: {height}, Width: {width}")
    canvas.refresh()
    space_stars = random.randint(30, 50)
    coroutines = [blink(canvas, random.randint(1, height-2), random.randint(1, width-2), random.choice("+*.:")) for _ in range(space_stars)]

    rocket_symbols = get_rocket_frame()
    coroutines.append(fire(canvas, height/2, (width/2)+2))
    coroutines.append(animate_spaceship(canvas, height/2, width/2, rocket_symbols))

    while coroutines:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        time.sleep(TIC_TIMEOUT)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(main)
