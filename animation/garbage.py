import random

from utils import draw_frame, get_frame_size, sleep


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    rows_number, columns_number = canvas.getmaxyx()
    frame_rows, frame_columns = get_frame_size(garbage_frame)

    column = max(column, 0)
    column = min(column, columns_number - frame_columns - 1)
    # column = max(column, min(column, columns_number - frame_columns - 1))
    row = 1

    while row + frame_rows < rows_number - 1:
        draw_frame(canvas, row, column, garbage_frame)
        await sleep()
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas, coroutines, garbage_frames, max_width):
    while True:
        column = random.randint(1, max_width - 2)
        time_stick = random.randint(10, 20)
        garbage_frame = random.choice(garbage_frames)
        coroutines.append(fly_garbage(canvas, column=column, garbage_frame=garbage_frame))
        await sleep(time_stick)