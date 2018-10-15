""" Graphics for Two Player Tetris """

from vpython import box, color, compound, sleep, scene, sphere, vector


def main():
    delta_t = 2
    columns, rows = 10, 24
    draw_board(columns, rows)
    first = Tetromino(0, 0)
    # first.update_tetromino('I', 'Horizontal')
    for shape in ['T', 'I', 'O', 'S', 'J', 'Z', 'L']:
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


class Tetromino:
    """ Types I, O, S, Z, T, J, L """

    def __init__(self, x, y, shape='O', colour=color.white, player='first'):
        self.x_pos = x
        self.y_pos = y
        self.shape = shape
        self.color = colour
        self.orientation = '0'
        self.blocks = []
        radius = 0.23 if player == 'first' else 0.22
        for _ in range(4):
            block = compound([box(pos=vector(x, y, 0), height=.8, width=.8, length=.8),
                             sphere(pos=vector(x, y, 0.5), radius=radius),
                             sphere(pos=vector(x, y, -0.5), radius=radius)])
            self.blocks.append(block)
        self.shape_dictionary = {
                                 ('I', '0'): (0, 0, 1, 0, 2, 0, 3, 0),
                                 ('I', '1'): (0, 0, 0, 1, 0, 2, 0, 3),
                                 ('I', '2'): (0, 0, 1, 0, 2, 0, 3, 0),
                                 ('I', '3'): (0, 0, 0, 1, 0, 2, 0, 3),
                                 ('J', '0'): (0, 0, 0, 1, 1, 0, 2, 0),
                                 ('J', '1'): (0, 0, 1, 0, 1, 1, 1, 2),
                                 ('J', '2'): (0, 1, 1, 1, 2, 1, 2, 0),
                                 ('J', '3'): (0, 0, 0, 1, 0, 2, 1, 2),
                                 ('T', '0'): (0, 0, 1, 0, 2, 0, 1, 1),
                                 ('T', '1'): (1, 0, 1, 1, 1, 2, 0, 1),
                                 ('T', '2'): (0, 1, 1, 1, 2, 1, 1, 0),
                                 ('T', '3'): (0, 0, 0, 1, 0, 2, 1, 1),
                                 ('S', '0'): (0, 0, 1, 0, 1, 1, 2, 1),
                                 ('S', '1'): (1, 0, 1, 1, 0, 1, 0, 2),
                                 ('S', '2'): (0, 0, 1, 0, 1, 1, 2, 1),
                                 ('S', '3'): (1, 0, 1, 1, 0, 1, 0, 2),
                                 ('Z', '0'): (0, 1, 1, 1, 1, 0, 2, 0),
                                 ('Z', '1'): (0, 0, 0, 1, 1, 1, 1, 2),
                                 ('Z', '2'): (0, 1, 1, 1, 1, 0, 2, 0),
                                 ('Z', '3'): (0, 0, 0, 1, 1, 1, 1, 2),
                                 ('O', '0'): (0, 0, 1, 0, 0, 1, 1, 1),
                                 ('O', '1'): (0, 0, 1, 0, 0, 1, 1, 1),
                                 ('O', '2'): (0, 0, 1, 0, 0, 1, 1, 1),
                                 ('O', '3'): (0, 0, 1, 0, 0, 1, 1, 1),
                                 ('L', '0'): (0, 0, 1, 0, 2, 0, 2, 1),
                                 ('L', '1'): (1, 0, 1, 1, 1, 2, 0, 2),
                                 ('L', '2'): (0, 0, 0, 1, 1, 1, 2, 1),
                                 ('L', '3'): (0, 0, 1, 0, 0, 1, 0, 2),
                                 }
        self.updater(self.x_pos, self.y_pos, orientation=self.orientation)

    def updater(self, x, y, shape=None, orientation=None):
        if shape:
            self.shape = shape
        else:
            shape = self.shape
        if orientation:
            self.orientation = orientation
        else:
            orientation = self.orientation

        self.y_pos = y
        self.x_pos = x
        coor_list = self.shape_dictionary[shape, orientation]
        for num in range(4):
            self.blocks[num].pos = vector(x, y, 0) + vector(coor_list[2 * num], coor_list[2 * num + 1], 0)
            self.blocks[num].color = self.color

    def __call__(self, x, y, shape, orientation, colour):
        self.shape = shape
        self.color = colour
        self.updater(x, y, orientation=orientation)


def draw_board(columns, rows):
    """ The board is a dictionary of cubes with coordinates as keys """
    scene.center = vector(int((columns - 1) / 2), int(rows / 2), 0)
    x_coordinates, y_coordinates = list(range(columns)), list(range(rows))
    board = {(x, y): box(pos=vector(x, y, 0), height=.8, width=.8, length=.8, opacity=0.2)
             for x in x_coordinates for y in y_coordinates}
    for item in board:
        board[item].status = False
    board[(-1, -1)] = columns, rows  # Board size gets stored in the board with key (-1, -1)

    return board


def change_cube_state(board, x_coordinate, y_coordinate, colour=color.white, opacity=1, status=True, visible=True):
    item = board.get((x_coordinate, y_coordinate))
    item.visible = visible
    item.opacity = opacity
    item.color = colour
    item.status = status


def update_board(board, board_status):
    columns, rows = board.get((-1, -1))  # Board size is stored in the board with key (-1, -1)
    for y in range(rows):
        for x in range(columns):
            cube = board.get((x, y))
            cube.visible, cube.color, cube.opacity = board_status.get((x, y))


if __name__ == '__main__':
    main()
