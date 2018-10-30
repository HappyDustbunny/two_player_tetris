

from vpython import color, scene, sleep, vector

from random import shuffle

from graphics import change_cube_state, draw_board, show_points, Tromino


class Player:
    def __init__(self, soft_drop, hard_drop, left, right, colour, player_number):
        """ Inputs define which keys to use: Player(a,s,w,d,...)
            player can be 'first' or 'second' Needed to discern players in case of overlap """
        self.player_number = player_number
        self.inputs = {
            # This dictionary stores the functions for navigation as tuples with (functions, argument)
            soft_drop: (self.nat_drop, None),
            hard_drop: (self.hard_drop, None),
            left: (self.move_tromino, -1),
            right: (self.move_tromino, 1),
        }
        self.bag = list('_Ibdpq')
        shuffle(self.bag)
        self.tromino = Tromino(5, 20, self.bag.pop(0), colour=colour, player=self.player_number, opacity=1)
        self.next_tromino = Tromino(-5 if player_number == 'first' else 15, 16, self.bag.pop(0),
                                        colour=colour, player=player_number)
        self.shadow = Tromino(5, 20, self.tromino.shape, colour=colour, player=self.player_number, opacity=0.5)

    def receive_input(self, board, received_inputs):
        action_input = None
        for inp in received_inputs:
            if self.inputs.get(inp):  # Inputs not bound to actions is ignored here
                action_input = self.inputs[inp]
        if action_input:
            action_input[0](board, action_input[1]) # The dictionary for actions stores tuples with (function, argument)
            # self.update_shadow(board)

    def move_tromino(self, board, move_dir):
        if self.probe(board, self.tromino.x_pos + move_dir, self.tromino.y_pos):
            self.tromino.updater(self.tromino.x_pos + move_dir, self.tromino.y_pos)

    def nat_drop(self, board, action_input=None):
        if self.probe(board, self.tromino.x_pos, self.tromino.y_pos - 1):
            self.tromino.updater(self.tromino.x_pos, self.tromino.y_pos - 1)
        else:
            loss_check = self.landing_procedure(board)
            return loss_check

    def hard_drop(self, board, action_input=None):
        for y in range(self.tromino.y_pos, -1, -1):
            if self.probe(board, self.tromino.x_pos, y) and not self.probe(board, self.tromino.x_pos, y - 1):
                self.tromino.updater(self.tromino.x_pos, y)
                return

    def landing_procedure(self, board):
        affected_lines = []
        for block in self.tromino.blocks:
            x, y = block.pos.x, block.pos.y
            if y not in affected_lines:
                affected_lines.append(y)
            change_cube_state(board, x, y, colour=self.tromino.color, opacity=1, status=True, visible=True)
        line_check(board, affected_lines)

        shape = self.next_tromino.shape
        if self.probe(board, x=3, y=21, shape=shape):
            self.tromino.updater(3, y=21, shape=shape)
            if not self.bag:
                self.bag = list('_Ibdpq')
                shuffle(self.bag)
            shape = self.bag.pop(0)
            self.next_tromino.updater(x=self.next_tromino.x_pos, y=self.next_tromino.y_pos, shape=shape)
        else:
            return 'FAILURE'

    def update_shadow(self, board):
        for y in range(self.tromino.y_pos, -1, -1):
            if self.probe(board, self.tromino.x_pos, y) and not self.probe(board, self.tromino.x_pos, y - 1):
                self.shadow.updater(self.tromino.x_pos, y, shape=self.tromino.shape)
                return

    def probe(self, board, x, y, shape=None):
        if not shape:
            shape = self.tromino.shape
        coor_list = self.tromino.shape_dictionary[shape]
        for num in range(3):
            probing_coor = x + coor_list[2 * num], y + coor_list[2 * num + 1]
            if not board.get(probing_coor):  # Checks if coordinate is in the board
                return False
            if board.get(probing_coor).status:
                return False
        return True


def line_check(board, check_lines):
    cleared_lines = 0
    all_checked = False
    while not all_checked:
        all_checked = True
        for line in check_lines:
            line_full = True
            inted_line = int(line)
            for x in range(board['width']):
                if not board[(x, inted_line)].status:
                    line_full = False
            if line_full:
                clear_lines(board, inted_line)
                cleared_lines += 1
                all_checked = False
    if cleared_lines > 0:
        score(board, cleared_lines)
        # It will only get here in the recursion loop where it finds no more clearable lines.


def score(board, lines_cleared):
    points = {0: 0, 1: 100, 2: 300, 3: 600}[lines_cleared] * int(board['level'])
    board['points'] += points
    board['level'] += lines_cleared * .1
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
    player = Player('s', 'w', 'a', 'd', color.red, player_number='first')
    # blue_player = Player('k', 'i', 'j', 'l', color.blue, player_number='second')
    # players = [red_player, blue_player]
    scene.bind('keydown', capture_key)
    columns, rows = 8, 24
    board = draw_board(columns, rows)
    scene.center = vector(int(columns / 2), int(rows / 2) - 3, 0)
    scene.range = columns + 2
    scene.autoscale = False

    while True:
        for _ in range(5):
            sleep((0.16 - int(board['level']) * 0.01) if board['level'] <= 15 else 0.01)
            received_inputs = Key_Event
            player.receive_input(board, received_inputs)
            player.update_shadow(board)
            Key_Event = []
        loss_check = player.nat_drop(board)
        if loss_check == 'FAILURE':
            return
        player.update_shadow(board)


if __name__ == '__main__':
    main()
