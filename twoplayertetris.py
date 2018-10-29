""" Two Player Tetris  """

from vpython import color, scene, sleep, vector

from random import shuffle

from graphics import change_cube_state, draw_board, show_points, Tetromino


class Player:
    def __init__(self, turn_widdershins, turn_clockwise, soft_drop, hard_drop, left, right, colour, player_number):
        """ Inputs define which keys to use: Player(a,s,w,d,...)
            player can be 'first' or 'second' Needed to discern players in case of overlap """
        self.player_number = player_number
        self.inputs = {
            # This dictionary stores the functions for navigation as tuples with (functions, argument)
            turn_widdershins: (self.turn_tetromino, -1),
            turn_clockwise: (self.turn_tetromino, 1),
            soft_drop: (self.nat_drop, None),
            hard_drop: (self.hard_drop, None),
            left: (self.move_tetromino, -1),
            right: (self.move_tetromino, 1),
        }
        self.bag = list('IOTSZJL')
        shuffle(self.bag)
        self.tetromino = Tetromino(5, 20, self.bag.pop(0), colour=colour, player=self.player_number)
        self.next_tetromino = Tetromino(-5 if player_number == 'first' else 15, 16, self.bag.pop(0),
                                        colour=colour, player=player_number)

    def receive_input(self, board, received_inputs):
        action_input = None
        for inp in received_inputs:
            if self.inputs.get(inp): # Inputs not bound to actions is ignored here
                action_input = self.inputs[inp]
        if action_input:
            action_input[0](board, action_input[1]) # The dictionary for actions stores tuples with (function, argument)

    def move_tetromino(self, board, move_dir):
        if self.probe(board, self.tetromino.x_pos + move_dir, self.tetromino.y_pos):
            self.tetromino.updater(self.tetromino.x_pos + move_dir, self.tetromino.y_pos)

    def turn_tetromino(self, board, turn_dir):
        # TODO: The turning isn't up to the official standards for how tetrominoes are supposed to turn.
        new_ori = str((int(self.tetromino.orientation) + turn_dir) % 4)
        modifier_tuple = ((0, 0), (-1, 0), (1, 0), (0, -1))
        for x_mod, y_mod in modifier_tuple:
            if self.probe(board, self.tetromino.x_pos + x_mod, self.tetromino.y_pos + y_mod, orientation=new_ori):
                self.tetromino.updater(self.tetromino.x_pos + x_mod, self.tetromino.y_pos + y_mod, orientation=new_ori)
                return
        # TODO: As is, the I tetromino refuses to use move itself to turn if it's too close to a wall.

    def nat_drop(self, board, action_input=None):
        if self.probe(board, self.tetromino.x_pos, self.tetromino.y_pos - 1):
            self.tetromino.updater(self.tetromino.x_pos, self.tetromino.y_pos - 1)
        else:
            loss_check = self.landing_procedure(board)
            return loss_check

    def hard_drop(self, board, action_input=None):
        for y in range(self.tetromino.y_pos, -1, -1):
            if self.probe(board, self.tetromino.x_pos, y) and not self.probe(board, self.tetromino.x_pos, y - 1):
                self.tetromino.updater(self.tetromino.x_pos, y)
                return

    def landing_procedure(self, board):
        affected_lines = []
        for num in range(4):
            x, y = self.tetromino.blocks[num].pos.x, self.tetromino.blocks[num].pos.y
            if y not in affected_lines:
                affected_lines.append(y)
            change_cube_state(board, x, y, colour=self.tetromino.color, opacity=1, status=True, visible=True)
        line_check(board, affected_lines)

        shape = self.next_tetromino.shape
        if self.probe(board, x=4, y=21, shape=shape, orientation='0'):
            self.tetromino.updater(4, y=21, shape=shape, orientation='0')
            if not self.bag:
                self.bag = list('IOTSZJL')
                shuffle(self.bag)
            shape = self.bag.pop(0)
            self.next_tetromino.updater(x=self.next_tetromino.x_pos, y=self.next_tetromino.y_pos, shape=shape)
        else:
            return 'FAILURE'

    def probe(self, board, x, y, shape=None, orientation=None):
        if not shape:
            shape = self.tetromino.shape
        if not orientation:
            orientation = self.tetromino.orientation

        coor_list = self.tetromino.shape_dictionary[shape, orientation]
        for num in range(4):
            probing_coor = x + coor_list[2 * num], y + coor_list[2 * num + 1]
            if not board.get(probing_coor):  # Checks if coordinate is in the board
                return False
            if board.get(probing_coor).status:
                return False
        return True


def line_check(board, check_lines, combo=0):
    for line in check_lines:
        line_full = True
        inted_line = int(line)
        for x in range(board['width']):
            if not board[(x, inted_line)].status:
                line_full = False
        if line_full:
            clear_lines(board, inted_line)
            line_check(board, check_lines, combo + 1)
            return
    if combo != 0:
        score(board, combo)
        # It will only get here in the recursion loop where it finds no more clearable lines.


def score(board, lines_cleared):
    points = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}[lines_cleared] * board['level']
    board['points'] += points
    print(board['points'])
    show_points(board, board['points'])


def clear_lines(board, line_to_clear):
    for drop_to_line in range(line_to_clear, int(board['height']) - 1):
        for x in range(board['width']):
            block_above = board[(x, drop_to_line + 1)]
            change_cube_state(board, x_coordinate=x, y_coordinate=drop_to_line, colour=block_above.color,
                              opacity=block_above.opacity, status=block_above.status, visible=block_above.visible)
    # As is, it won't update the topmost line, it will merely copy it onto the line below.
    # This shouldn't be an issue, since the topmost line should always be empty, but it could maybe cause problems.


Key_Event = []


def capture_key(event):
    global Key_Event
    Key_Event.append(event.key)


def main():
    global Key_Event
    red_player = Player('q', 'e', 's', 'w', 'a', 'd', color.red, player_number='first')
    blue_player = Player('u', 'o', 'k', 'i', 'j', 'l', color.blue, player_number='second')
    players = [red_player, blue_player]
    scene.bind('keydown', capture_key)
    columns, rows = 10, 24
    board = draw_board(columns, rows)
    scene.center = vector(int(columns / 2), int(rows / 2) - 3, 0)
    scene.range = columns + 2
    scene.autoscale = False

    while True:
        for _ in range(5):
            sleep(0.5)
            # sleep(0.15)
            received_inputs = Key_Event
            for player in players:
                player.receive_input(board, received_inputs)
            Key_Event = []
        for player in players:
            loss_check = player.nat_drop(board)
            if loss_check == 'FAILURE':
                return


if __name__ == '__main__':
    main()
