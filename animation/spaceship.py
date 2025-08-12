import asyncio
from itertools import cycle

from utils import draw_frame, get_frame_size, read_controls


async def animate_spaceship(canvas, start_row, start_column, rocket_symbols):
    prev_frame = None
    row, column = start_row, start_column
    prev_row, prev_column = row, column
    frame_rows, frame_columns = get_frame_size(rocket_symbols[0])
    max_row, max_column = canvas.getmaxyx()

    for frame in cycle(rocket_symbols):
        rows_direction, columns_direction, _ = read_controls(canvas)
        row += rows_direction
        column += columns_direction

        row = max(1, min(row + rows_direction, max_row - frame_rows - 1))
        column = max(1, min(column + columns_direction, max_column - frame_columns - 1))

        if prev_frame is not None:
            draw_frame(canvas, prev_row, prev_column, prev_frame, negative=True)
        draw_frame(canvas, row, column, frame)

        canvas.refresh()
        prev_frame = frame
        prev_row, prev_column = row, column

        for _ in range(2):
            await asyncio.sleep(0)