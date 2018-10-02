""" Graphics for Two Player Tetris """

from vpython import box, color, sleep, scene, vector


def main():
    delta_t = 1.2
    columns, rows = 10, 24
    draw_board(columns, rows)
    first = Tetramino(0, 0)
    # first.update_tetramino('I', 'Horizontal')
    for shape in ['T', 'I', 'O', 'S', 'Z', 'J', 'L']:
        for count in range(4):
            first(0, 0, shape, str(count), color.cyan)
            sleep(delta_t)
    #     i = 0
    # for _ in range(0, 190, 10):
    #     i += 1
    #     i %= 4
    #     print(i)
    #     first(10, 200 - _, 'T', str(i))
    #     sleep(delta_t)
    # x_coordinates, y_coordinates = list(range(columns)), list(range(rows))
    # board_status = {(x, y): (True, color.cyan, 1) for x in x_coordinates for y in y_coordinates}
    # update_board(board, board_status)
    # sleep(1)
    # change_cube_state(board, 1, 2, color.red, 1, True)
    # while True:
    #     board_status = {(x, y): (True, vector(random(), random(), random()), 1) for x in x_coordinates for y in
    #                     y_coordinates}
    #     update_board(board, board_status)
    #     sleep(0.1)


class Tetramino:
    """ Types I, O, S, Z, T, J, L """

    def __init__(self, x, y, shape='O', colour=color.white):
        self.x_pos = 10 * x
        self.y_pos = 10 * y
        self.shape = shape
        self.color = colour
        self.orientation = '1'
        self.boxes = []
        for _ in range(4):
            self.boxes.append(box(pos=vector(x, y, 0), height=8, width=8, length=8))

    def __call__(self, x, y, shape, orientation='0', colour=color.white):
        self.shape = shape
        print(colour)

        for num in range(4):
            self.boxes[num].pos = vector(x * 10, y * 10, 0)

        shape_dictionary = {('I', '0'): (0, 0, 10, 0, 20, 0, 30, 0),
                            ('I', '1'): (0, 0, 0, 10, 0, 20, 0, 30),
                            ('I', '2'): (0, 0, 10, 0, 20, 0, 30, 0),
                            ('I', '3'): (0, 0, 0, 10, 0, 20, 0, 30),
                            ('J', '0'): (0, 0, 0, 10, 0, 20, 10, 20),
                            ('J', '1'): (20, 0, 20, 10, 10, 10, 0, 10),
                            ('J', '2'): (0, 0, 10, 0, 10, 10, 10, 20),
                            ('J', '3'): (0, 0, 10, 0, 20, 0, 0, 10),
                            ('L', '0'): (0, 0, 10, 0, 0, 10, 0, 20),
                            ('L', '1'): (10, 0, 10, 10, 10, 20, 0, 20),
                            ('L', '2'): (0, 0, 0, 10, 10, 10, 20, 10),
                            ('L', '3'): (0, 0, 10, 0, 20, 0, 20, 10),
                            ('S', '0'): (0, 0, 10, 0, 10, 10, 20, 10),
                            ('S', '1'): (10, 0, 10, 10, 0, 10, 0, 20),
                            ('S', '2'): (0, 0, 10, 0, 10, 10, 20, 10),
                            ('S', '3'): (10, 0, 10, 10, 0, 10, 0, 20),
                            ('Z', '0'): (0, 10, 10, 10, 10, 0, 20, 0),
                            ('Z', '1'): (0, 10, 10, 10, 10, 0, 20, 0),
                            ('Z', '2'): (0, 0, 0, 10, 10, 10, 10, 20),
                            ('Z', '3'): (0, 0, 0, 10, 10, 10, 10, 20),
                            ('O', '0'): (0, 0, 10, 0, 0, 10, 10, 10),
                            ('O', '1'): (0, 0, 10, 0, 0, 10, 10, 10),
                            ('O', '2'): (0, 0, 10, 0, 0, 10, 10, 10),
                            ('O', '3'): (0, 0, 10, 0, 0, 10, 10, 10),
                            ('T', '0'): (0, 0, 10, 0, 20, 0, 10, 10),
                            ('T', '1'): (10, 0, 10, 10, 10, 20, 0, 10),
                            ('T', '2'): (10, 0, 0, 10, 10, 10, 20, 10),
                            ('T', '3'): (0, 0, 0, 10, 0, 20, 10, 10),
                            }
        coordinate_list = shape_dictionary[shape, orientation]
        for num in range(4):
            self.boxes[num].pos += vector(coordinate_list[2 * num], coordinate_list[2 * num + 1], 0)
            self.boxes[num].color = colour


def draw_board(columns, rows):
    """ The board is a dictionary of cubes with coordinates as keys """
    scene.center = vector(int(10 * (columns - 1) / 2), int(10 * rows / 2), 0)
    x_coordinates, y_coordinates = list(range(columns)), list(range(rows))
    board = {(x, y): box(pos=vector(10 * x, 10 * y, 0), height=8, width=8, length=8, opacity=0.2)
             for x in x_coordinates for y in y_coordinates}
    board[(-1, -1)] = columns, rows  # Board size gets stored in the board with key (-1, -1)
    print('Board drawn')

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
