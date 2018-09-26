""" Graphics for Two Player Tetris """

from vpython import box, color, random, sleep, scene, vector


def main():
    columns, rows = 20, 50 # 10, 24
    board = draw_board(columns, rows)
    x_coordinates, y_coordinates = list(range(columns)), list(range(rows))
    # board_status = {(x, y): (True, color.cyan, 1) for x in x_coordinates for y in y_coordinates}
    # update_board(board, board_status)
    # sleep(1)
    # change_cube_state(board, 1, 2, color.red, 1, True)
    while True:
        board_status = {(x, y): (True, vector(random(), random(), random()), 1) for x in x_coordinates for y in
                        y_coordinates}
        update_board(board, board_status)
        # sleep(0.1)


def draw_board(columns, rows):
    """ The board is a dictionary of cubes with coordinates as keys """
    scene.center = vector(int(10 * (columns - 1)/2), int(10 * rows/2), 0)
    x_coordinates, y_coordinates = list(range(columns)), list(range(rows))
    board = {(x, y): box(pos=vector(10 * x, 10 * y, 0), height=8, width=8, length=8, opacity=0.2, visible=True)
             for x in x_coordinates for y in y_coordinates}
    board[(-1, -1)] = columns, rows  # Board size gets stored in the board with key (-1, -1)

    return board


def change_cube_state(board, x_coordinate, y_coordinate, colour=color.white, opacity=1, visible=True):
    item = board.get((x_coordinate, y_coordinate))
    item.visible = visible
    item.opacity = opacity
    item.color = colour


def update_board(board, board_status):
    columns, rows = board.get((-1, -1))  # Board size is stored in the board with key (-1, -1)
    for y in range(rows):
        for x in range(columns):
            cube = board.get((x, y))
            cube.visible, cube.color, cube.opacity = board_status.get((x, y))


if __name__ == '__main__':
    main()
