""" Graphics for Two Player Tetris """

from vpython import box, color, compound, sleep, scene, sphere, vector, text


def main():
    print('This is just graphics modules for twoplayertetris.py and trotris.py  ')


class Tetromino:
    """ Types I, O, S, Z, T, J, L """

    def __init__(self, x, y, shape='O', colour=color.white, player='first', opacity=1):
        self.x_pos = x
        self.y_pos = y
        self.shape = shape
        self.color = colour
        self.orientation = '0'
        self.blocks = []
        radius = 0.23 if player == 'first' else 0.22
        for _ in range(4):
            block = compound([box(pos=vector(x, y, 0), height=.8, width=.8, length=.8, opacity=opacity),
                              sphere(pos=vector(x, y, 0.5), radius=radius, opacity=opacity),
                              sphere(pos=vector(x, y, -0.5), radius=radius, opacity=opacity)])
            self.blocks.append(block)
        self.shape_dictionary = {
            ('I', '0'): (-1, 0, 0, 0, 1, 0, 2, 0),
            ('I', '1'): (0, -1, 0, 0, 0, 1, 0, 2),
            ('I', '2'): (-1, 0, 0, 0, 1, 0, 2, 0),
            ('I', '3'): (0, -1, 0, 0, 0, 1, 0, 2),
            ('J', '0'): (-1, 0, 0, 0, 1, 0, -1, 1),
            ('J', '1'): (0, -1, 0, 0, 0, 1, -1, -1),
            ('J', '2'): (-1, 0, 0, 0, 1, 0, 1, -1),
            ('J', '3'): (0, -1, 0, 0, 0, 1, 1, 1),
            ('T', '0'): (-1, 0, 0, 0, 1, 0, 0, 1),
            ('T', '1'): (0, 0, 0, -1, 0, 1, -1, 0),
            ('T', '2'): (-1, 0, 0, 0, 1, 0, 0, -1),
            ('T', '3'): (0, 0, 0, -1, 0, 1, 1, 0),
            ('S', '0'): (1, 0, 0, 0, 1, 1, 2, 1),
            ('S', '1'): (1, 1, 1, 0, 0, 1, 0, 2),
            ('S', '2'): (1, 0, 0, 0, 1, 1, 2, 1),
            ('S', '3'): (1, 1, 1, 0, 0, 1, 0, 2),
            ('Z', '0'): (1, 1, 0, 1, 1, 0, 2, 0),
            ('Z', '1'): (0, 1, 0, 0, 1, 1, 1, 2),
            ('Z', '2'): (1, 1, 0, 1, 1, 0, 2, 0),
            ('Z', '3'): (0, 1, 0, 0, 1, 1, 1, 2),
            ('O', '0'): (1, 0, 0, 0, 0, 1, 1, 1),
            ('O', '1'): (1, 0, 0, 0, 0, 1, 1, 1),
            ('O', '2'): (1, 0, 0, 0, 0, 1, 1, 1),
            ('O', '3'): (1, 0, 0, 0, 0, 1, 1, 1),
            ('L', '0'): (-1, 0, 0, 0, 1, 0, 1, 1),
            ('L', '1'): (0, -1, 0, 0, 0, 1, -1, 1),
            ('L', '2'): (-1, 0, 0, 0, 1, 0, -1, -1),
            ('L', '3'): (0, -1, 0, 0, 0, 1, 1, -1),
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


class Tromino:

    def __init__(self, x, y, shape='_', colour=color.white, player='first', opacity=1):
        self.x_pos = x
        self.y_pos = y
        self.shape = shape
        self.color = colour
        self.blocks = []
        radius = 0.23 if player == 'first' else 0.22
        for _ in range(3):
            block = compound([box(pos=vector(x, y, 0), height=.8, width=.8, length=.8, opacity=opacity),
                              sphere(pos=vector(x, y, 0.5), radius=radius, opacity=opacity),
                              sphere(pos=vector(x, y, -0.5), radius=radius, opacity=opacity)])
            self.blocks.append(block)
        self.shape_dictionary = {
            '_': (0, 0, 1, 0, 2, 0),
            'I': (0, 0, 0, 1, 0, 2),
            'b': (0, 0, 1, 0, 0, 1),
            'd': (0, 0, 1, 0, 1, 1),
            'p': (0, 0, 0, 1, 1, 1),
            'q': (0, 1, 1, 0, 1, 1),
        }
        self.updater(self.x_pos, self.y_pos)

    def updater(self, x, y, shape=None):
        if shape:
            self.shape = shape
        else:
            shape = self.shape
        self.y_pos = y
        self.x_pos = x
        coor_list = self.shape_dictionary[shape]
        for num in range(3):
            self.blocks[num].pos = vector(x, y, 0) + vector(coor_list[2 * num], coor_list[2 * num + 1], 0)
            self.blocks[num].color = self.color

    def __call__(self, x, y, shape, orientation, colour):
        self.color = colour
        self.updater(x, y, shape)


def draw_board(columns, rows):
    """ The board is a dictionary of cubes with coordinates as keys """
    scene.center = vector(int((columns - 1) / 2), int(rows / 2), 0)
    x_coordinates, y_coordinates = list(range(columns)), list(range(rows))
    board = {(x, y): box(pos=vector(x, y, 0), height=.8, width=.8, length=.8, opacity=0.2)
             for x in x_coordinates for y in y_coordinates}
    for item in board:
        board[item].status = False
    board['width'] = columns
    board['height'] = rows  # Board size gets stored in the board with key (-1, -1)
    board['level'] = 1
    board['points'] = 0
    board['point_display'] = text(pos=vector(-4, 18, 0), text='0', color=vector(0.6, 0.4, 0.8))
    board['GO_message1'] = text(pos=vector(int(columns / 2) - 4, int(rows / 2) - 3, 1), text=' GAME OVER! ',
                                color=color.green, visible=False)
    board['GO_message2'] = text(pos=vector(int(columns / 2) - 12, int(rows / 2) - 6, 1),
                                text=" Press any key to try again or 'e' to Exit ",
                                color=color.green, visible=False)

    return board


def change_cube_state(board, x_coordinate, y_coordinate, colour=color.white, opacity=1, status=True, visible=True):
    item = board.get((x_coordinate, y_coordinate))
    item.visible = visible
    item.opacity = opacity
    item.color = colour
    item.status = status


def show_points(board):
    board['point_display'].visible = False
    del (board['point_display'])
    board['point_display'] = text(pos=vector(-6, 18, 0), text=str(board['points']), color=vector(0.6, 0.4, 0.8))


def display_game_over(board, status):
    board['GO_message1'].visible = status
    board['GO_message2'].visible = status


if __name__ == '__main__':
    main()
