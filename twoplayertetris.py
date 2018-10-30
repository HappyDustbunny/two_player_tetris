""" Two Player Tetris  """

from vpython import box, color, scene, sleep, text, vector

from random import shuffle

from graphics import change_cube_state, display_game_over, draw_board, show_points, Tetromino, turn_board_off


class Player:
    def __init__(self, turn_widdershins, turn_clockwise, soft_drop, hard_drop, left, right, colour, player_number):
        """ Inputs define which keys to use: Player(a,s,w,d,...)
            player can be 'first' or 'second' Needed to discern players in case of overlap """
        self.player_number = player_number
        self.inputs = {
            # This dictionary stores the functions for navigation as tuples with (functions, argument)
            turn_widdershins: (self.turn_tetromino, 1),
            turn_clockwise: (self.turn_tetromino, -1),
            soft_drop: (self.nat_drop, None),
            hard_drop: (self.hard_drop, None),
            left: (self.move_tetromino, -1),
            right: (self.move_tetromino, 1),
        }
        self.bag = list('IOTSZJL')
        shuffle(self.bag)
        self.tetromino = Tetromino(5, 21, self.bag.pop(0), colour=colour, player=self.player_number, opacity=1)
        self.next_tetromino = Tetromino(-5 if player_number == 'first' else 15, 16, self.bag.pop(0),
                                        colour=colour, player=player_number)
        self.shadow = Tetromino(5, 20, self.tetromino.shape, colour=colour, player=self.player_number, opacity=0.5)

    def receive_input(self, board, received_inputs):
        action_input = None
        for inp in received_inputs:
            if self.inputs.get(inp):  # Inputs not bound to actions is ignored here
                action_input = self.inputs[inp]
        if action_input:
            action_input[0](board,
                            action_input[1])  # The dictionary for actions stores tuples with (function, argument)
            # self.update_shadow(board)

    def move_tetromino(self, board, move_dir):
        if self.probe(board, self.tetromino.x_pos + move_dir, self.tetromino.y_pos):
            self.tetromino.updater(self.tetromino.x_pos + move_dir, self.tetromino.y_pos)

    def turn_tetromino(self, board, turn_dir):
        # TODO: Check if turning is up to the official standards for how tetrominoes are supposed to turn.
        new_ori = str((int(self.tetromino.orientation) + turn_dir) % 4)
        modifier_list = [(0, 0), (-turn_dir, 0), (turn_dir, 0), (0, -1)]
        if self.tetromino.shape == 'I' and self.tetromino.orientation in '13':  # Ugly solution.
            modifier_list.append((-2, 0))
        for x_mod, y_mod in modifier_list:
            if self.probe(board, self.tetromino.x_pos + x_mod, self.tetromino.y_pos + y_mod, orientation=new_ori):
                self.tetromino.updater(self.tetromino.x_pos + x_mod, self.tetromino.y_pos + y_mod, orientation=new_ori)
                return

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
        for block in self.tetromino.blocks:
            x, y = block.pos.x, block.pos.y
            if y not in affected_lines:
                affected_lines.append(y)
            change_cube_state(board, x, y, colour=self.tetromino.color, opacity=1, status=True, visible=True)
        line_check(board, affected_lines)
        return self.move_to_top(board)

    def move_to_top(self, board):
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

    def update_shadow(self, board):
        for y in range(self.tetromino.y_pos, -1, -1):
            if self.probe(board, self.tetromino.x_pos, y) and not self.probe(board, self.tetromino.x_pos, y - 1):
                self.shadow.updater(self.tetromino.x_pos, y, shape=self.tetromino.shape,
                                    orientation=self.tetromino.orientation)
                return

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

    def reset_game(self, board):
        self.bag = list('IOTSZJL')
        shuffle(self.bag)
        self.next_tetromino.updater(x=self.next_tetromino.x_pos, y=self.next_tetromino.y_pos, shape=self.bag.pop(0))
        self.move_to_top(board)

    def turn_off_tetrominoes(self):  # Turn all tetrominoes off
        for block in self.tetromino.blocks:
            block.visible = False
        for block in self.next_tetromino.blocks:
            block.visible = False
        for block in self.shadow.blocks:
            block.visible = False


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
                clear_line(board, inted_line)
                cleared_lines += 1
                all_checked = False
    if cleared_lines > 0:
        score(board, cleared_lines)
        # It will only get here in the recursion loop where it finds no more clearable lines.


def score(board, lines_cleared):
    points = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}[lines_cleared] * int(board['level'])
    board['points'] += points
    board['level'] += lines_cleared * .1
    print(board['points'])
    show_points(board)


def clear_line(board, line_to_clear):
    for drop_to_line in range(line_to_clear, int(board['height']) - 1):
        for x in range(board['width']):
            block_above = board[(x, drop_to_line + 1)]
            change_cube_state(board, x_coordinate=x, y_coordinate=drop_to_line, colour=block_above.color,
                              opacity=block_above.opacity, status=block_above.status, visible=block_above.visible)
    # As is, it won't update the topmost line, it will merely copy it onto the line below.
    # This shouldn't be an issue, since the topmost line should always be empty, but it could maybe cause problems.


def game_over(board, players):
    display_game_over(board, True)  # Turn GAME OVER message on
    while True:
        received_inputs = Key_Event
        for event in received_inputs:
            if received_inputs:
                display_game_over(board, False)
            if event == 'e':  # Tidy up and exits game
                turn_board_off(board)
                for player in players:
                    player.turn_off_tetrominoes()
                text(pos=vector(int(board['width'] / 2) - 8, int(board['height'] / 2) - 3, 1), text=' Goodbye! ',
                     height=2.5, color=color.green)
                exit_status = True
                return exit_status
            else:
                # display_game_over(board, False)  # Tidy up and restart game
                for _ in range(board['height']):
                    clear_line(board, 0)
                board['level'], board['points'] = 1, 0
                show_points(board)
                for player in players:
                    player.reset_game(board)
                    player.update_shadow(board)
                return


Key_Event = []


def capture_key(event):
    global Key_Event
    Key_Event.append(event.key.lower())


def main():
    global Key_Event
    scene.bind('keydown', capture_key)
    end_of_game = False

    columns, rows = 10, 24

    scene.height = 550
    board = draw_board(columns, rows)
    scene.center = vector(int(columns / 2), int(rows / 2) - 3, 0)
    scene.range = columns + 2
    scene.autoscale = False

    red_player = Player('q', 'e', 's', 'w', 'a', 'd', color.red, player_number='first')
    blue_player = Player('u', 'o', 'k', 'i', 'j', 'l', color.blue, player_number='second')
    players = [red_player, blue_player]

    while not end_of_game:
        for _ in range(5):
            sleep((0.16 - int(board['level']) * 0.01) if board['level'] <= 15 else 0.01)
            received_inputs = Key_Event
            for player in players:
                player.receive_input(board, received_inputs)
            for player in players:
                player.update_shadow(board)
            Key_Event = []
        for player in players:
            loss_check = player.nat_drop(board)
            if loss_check == 'FAILURE':
                end_of_game = game_over(board, players)
            player.update_shadow(board)


if __name__ == '__main__':
    main()
