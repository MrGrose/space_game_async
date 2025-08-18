import asyncio
from pathlib import Path

from game_scenario import PHRASES

BASE_FOLDER = Path(__file__).parent / "frames"

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


def read_controls(canvas):
    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            break
        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1
        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1
        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


def get_frame_size(text):
    lines = text.splitlines()
    rows = len(lines)
    columns = max([len(line) for line in lines])
    return rows, columns


def get_rocket_frame():
    rocket_symbols = []
    path_file = BASE_FOLDER / "rocket_frame"
    for rocket in path_file.rglob("rocket_frame_*.txt"):
        with open(rocket, "r", encoding="utf-8") as file:
            rocket_symbols.append(file.read())

    return rocket_symbols


def draw_frame(canvas, start_row, start_column, text, negative=False):
    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue
        if row >= rows_number:
            break
        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue
            if column >= columns_number:
                break
            if symbol == " ":
                continue
            if row == rows_number - 1 and column == columns_number - 1:
                continue
            symbol = symbol if not negative else " "
            canvas.addch(row, column, symbol)


def get_garbage_frame():
    frames = []
    path_file = BASE_FOLDER / "garbage_frame"
    for garbage in path_file.rglob("*.txt"):
        with open(garbage, "r") as garbage_file:
            frames.append(garbage_file.read())

    return frames


async def sleep(tics=1):
    for _ in range(tics):
        await asyncio.sleep(0)


async def show_gameover(canvas, row, column, frame):
    height, width = canvas.getmaxyx()
    draw_frame(canvas, row, column, frame, negative=True)

    path_file = BASE_FOLDER / "gameover_frame/gameover.txt"
    with open(path_file, "r") as file:
        gameover_file = file.read()

    while True:
        draw_frame(canvas, height/2, width/3, gameover_file)
        await sleep()


async def update_year_counter(canvas, year_container):
    height, width = canvas.getmaxyx()
    while True:
        t = canvas.derwin(0, 0, height - 2, width - 100)
        year_container[0] += 1
        t.addstr(1, 1, f"Year: {year_container[0]} {PHRASES.get(year_container[0], '')}")
        await sleep(3)
