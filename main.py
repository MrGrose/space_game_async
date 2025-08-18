import curses
import random
import time

from animation.blink import blink
from animation.garbage import fill_orbit_with_garbage
from animation.spaceship import animate_spaceship
from utils import get_garbage_frame, get_rocket_frame, show_gameover

TIC_TIMEOUT = 0.1

coroutines, obstacles, obstacles_in_last_collisions = [], [], []


def main(canvas):
    global coroutines, obstacles, obstacles_in_last_collisions
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.border()
    height, width = canvas.getmaxyx()
    canvas.addstr(0, 0, f"Height: {height}, Width: {width}")
    space_stars = random.randint(30, 50)
    rocket_symbols = get_rocket_frame()
    garbage_frames = get_garbage_frame()

    coroutines.extend([blink(canvas, random.randint(1, height-2), random.randint(1, width-2), random.choice("+*.:"), random.randint(4, 10)) for _ in range(space_stars)])
    coroutines.append(animate_spaceship(canvas, height/2, width/2, rocket_symbols, coroutines, obstacles, obstacles_in_last_collisions))
    coroutines.append(fill_orbit_with_garbage(canvas, coroutines, garbage_frames, width, obstacles, obstacles_in_last_collisions))

    while coroutines:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(main)
