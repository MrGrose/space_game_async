from itertools import cycle

from animation.fire import fire
from physics import update_speed
from utils import draw_frame, get_frame_size, read_controls, sleep


async def animate_spaceship(canvas, start_row, start_column, rocket_symbols, coroutines, obstacles, obstacles_in_last_collisions):
    prev_frame = None
    row, column = start_row, start_column
    prev_row, prev_column = row, column
    frame_rows, frame_columns = get_frame_size(rocket_symbols[0])
    max_row, max_column = canvas.getmaxyx()
    row_speed = column_speed = 0
    for frame in cycle(rocket_symbols):
        for _ in range(2):
            rows_direction, columns_direction, space_pressed = read_controls(canvas)
            row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction, columns_direction,)
            row += rows_direction
            column += columns_direction

            row = max(1, min(row + rows_direction + row_speed, max_row - frame_rows - 1))
            column = max(1, min(column + columns_direction + column_speed, max_column - frame_columns - 1))

            if space_pressed:
                coroutines.append(fire(canvas, row, column+2, obstacles, obstacles_in_last_collisions, rows_speed=-0.99))

            if prev_frame is not None:
                draw_frame(canvas, prev_row, prev_column, prev_frame, negative=True)
            draw_frame(canvas, row, column, frame)

            prev_frame = frame
            prev_row, prev_column = row, column

            await sleep()