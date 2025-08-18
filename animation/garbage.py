import random

from animation.explosion import explode
from obstacles import Obstacle
from utils import draw_frame, get_frame_size, sleep


async def fly_garbage(canvas, column, garbage_frame, obstacles, obstacles_in_last_collisions, speed=0.5):

    rows_number, columns_number = canvas.getmaxyx()
    frame_rows, frame_columns = get_frame_size(garbage_frame)

    column = max(column, 0)
    column = min(column, columns_number - frame_columns - 1)
    # column = max(column, min(column, columns_number - frame_columns - 1))
    row = 1

    obstacle = Obstacle(row, column, frame_rows, frame_columns)
    obstacles.append(obstacle)

    try:
        while row + frame_rows < rows_number - 1:
            if obstacle in obstacles_in_last_collisions:
                obstacles_in_last_collisions.remove(obstacle)
                await explode(canvas, obstacle.row, obstacle.column)
                return
            else:
                obstacle.row = row
                obstacle.column = column
                draw_frame(canvas, row, column, garbage_frame)
                await sleep()
                draw_frame(canvas, row, column, garbage_frame, negative=True)
                row += speed
    finally:
        obstacles.remove(obstacle)


async def fill_orbit_with_garbage(canvas, coroutines, garbage_frames, max_width, obstacles, obstacles_in_last_collisions):
    while True:
        column = random.randint(1, max_width - 2)
        time_stick = random.randint(10, 20)
        garbage_frame = random.choice(garbage_frames)
        coroutines.append(fly_garbage(canvas, column=column, garbage_frame=garbage_frame, obstacles=obstacles, obstacles_in_last_collisions=obstacles_in_last_collisions))

        await sleep(time_stick)