import curses

from utils import sleep


async def fire(canvas, start_row, start_column, obstacles, obstacles_in_last_collisions, rows_speed=-0.3, columns_speed=0):
    row, column = start_row, start_column
    canvas.addstr(round(row), round(column), "*")
    await sleep()

    canvas.addstr(round(row), round(column), "O")
    await sleep()
    canvas.addstr(round(row), round(column), " ")

    row += rows_speed
    column += columns_speed

    symbol = "-" if columns_speed else "|"

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 1 < row < max_row and 1 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await sleep()
        canvas.addstr(round(row), round(column), " ")
        row += rows_speed
        column += columns_speed

        for obstacle in obstacles:
            if not obstacle.has_collision(row, column):
                continue
            else:
                obstacles_in_last_collisions.append(obstacle)
                return