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
            if self.inputs.get(inp):
                action_input = self.inputs[inp]
        if action_input:
            action_input[0](board, action_input[1])

    def move_tetromino(self, board, action_input):
        if self.probe(board, self.tetromino.x_pos + action_input, self.tetromino.y_pos):
            self.tetromino.updater(self.tetromino.x_pos + action_input, self.tetromino.y_pos)

    def turn_tetromino(self, board, action_input, hope=3):
        # TODO: The turning isn't up to the official standards for how tetrominoes are supposed to turn.
        new_ori = str((int(self.tetromino.orientation) + action_input) % 4)
        if self.probe(board, self.tetromino.x_pos, self.tetromino.y_pos, orientation=new_ori):
            self.tetromino.updater(self.tetromino.x_pos, self.tetromino.y_pos, orientation=new_ori)
            return
        if hope == 3:
            self.tetromino.x_pos -= 1
            self.turn_tetromino(action_input, board, hope=2)
        elif hope == 2:
            self.tetromino.x_pos += 2
            self.turn_tetromino(action_input, board, hope=1)
        elif hope == 1:
            self.tetromino.x_pos -= 1
            self.tetromino.y_pos -= 1
            self.turn_tetromino(action_input, board, hope=0)
        elif hope == 0:
            self.tetromino.y_pos += 1

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
        if shape == 'I':
            x = 3
        else:
            x = 4
        if self.probe(board, x=x, y=21, shape=shape, orientation='0'):
            self.tetromino.updater(x, y=21, shape=shape, orientation='0')
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


def score(board, lines_cleared):
    point_dict = {0: 100, 1: 300, 2: 500, 3: 800}
    points = point_dict[lines_cleared] * board['level']  # The level is stored in board with key 'level'
    board['points'] += points
    print(board['points'])
    show_points(board, board['points'])


def line_check(board, check_lines, combo=0):
    for line in check_lines:
        line_full = True
        inted_line = int(line)
        for x in range(board['width']):
            if not board[(x, inted_line)].status:
                line_full = False
        if line_full:
            clear_lines(board, inted_line)
            score(board, inted_line)
            line_check(board, check_lines, combo + 1)
            return
    if combo:
        score(board, combo)
        # It will only get here in the recursion loop where it finds no more clearable lines.


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
            sleep(0.15)
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
