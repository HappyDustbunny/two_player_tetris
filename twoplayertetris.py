""" Two Player Tetris  """

from vpython import color, scene, sleep, vector

from random import shuffle

from graphics import change_cube_state, draw_board, Tetromino


class Player:
    def __init__(self, turn_widdershins, turn_clockwise, soft_drop, hard_drop, left, right, colour, player):
        """ Inputs define which keys to use: Player(a,s,w,d,...)
            player can be 'first' or 'second' Needed to discern players in case of overlap """
        self.player = player
        self.inputs = {turn_widdershins: 'turn_ws', turn_clockwise: 'turn_cw',
                       soft_drop: 's_drop', hard_drop: 'h_drop', left: -1, right: 1}
        self.bag = list('IOTSZJL')
        shuffle(self.bag)
        self.tetromino = Tetromino(5, 20, self.bag.pop(0), colour=colour, player=self.player)

    def receive_input(self, board, received_inputs):
        action_input = None
        for inp in received_inputs:
            if self.inputs.get(inp):
                action_input = self.inputs[inp]
        if action_input == 's_drop':
            self.nat_drop(board)
        elif action_input == 'h_drop':
            self.hard_drop(board)
        elif action_input in (-1, 1):  # -1 and 1 are left and right, respectively
            self.move_tetromino(action_input, board)
        elif action_input in ('turn_ws', 'turn_cw'):
            self.turn_tetromino(action_input, board)

    def move_tetromino(self, action_input, board):
        if self.probe(board, self.tetromino.x_pos + action_input, self.tetromino.y_pos):
            self.tetromino.updater(self.tetromino.x_pos + action_input, self.tetromino.y_pos)

    def turn_tetromino(self, action_input, board, hope=3):
        # TODO: The turning isn't up to the official standards for how tetrominoes are supposed to turn.
        if action_input == 'turn_ws':
            if self.tetromino.orientation == '0':
                if self.probe(board, self.tetromino.x_pos, self.tetromino.y_pos, orientation='3'):
                    self.tetromino.updater(self.tetromino.x_pos, self.tetromino.y_pos, orientation='3')
                    return
            else:
                new_ori = str(int(self.tetromino.orientation) - 1)
                if self.probe(board, self.tetromino.x_pos, self.tetromino.y_pos, orientation=new_ori):
                    self.tetromino.updater(self.tetromino.x_pos, self.tetromino.y_pos, orientation=new_ori)
                    return
        if action_input == 'turn_cw':
            if self.tetromino.orientation == '3':
                if self.probe(board, self.tetromino.x_pos, self.tetromino.y_pos, orientation='0'):
                    self.tetromino.updater(self.tetromino.x_pos, self.tetromino.y_pos, orientation='0')
                    return
            else:
                new_ori = str(int(self.tetromino.orientation) + 1)
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

    def nat_drop(self, board):
        if self.probe(board, self.tetromino.x_pos, self.tetromino.y_pos - 1):
            self.tetromino.updater(self.tetromino.x_pos, self.tetromino.y_pos - 1)
        else:
            self.landing_procedure(board)

    def hard_drop(self, board):
        for y in range(self.tetromino.y_pos, -1, -1):
            if self.probe(board, self.tetromino.x_pos, y) and not self.probe(board, self.tetromino.x_pos, y - 1):
                self.tetromino.updater(self.tetromino.x_pos, y)
                return

    def landing_procedure(self, board):
        for num in range(4):
            x, y = self.tetromino.blocks[num].pos.x, self.tetromino.blocks[num].pos.y
            colour = self.tetromino.color
            change_cube_state(board, x, y, colour=colour, opacity=1, status=True, visible=True)
        if not self.bag:
            self.bag = list('IOTSZJL')
            shuffle(self.bag)
        shape = self.bag.pop(0)
        if shape == 'I':
            x = 3
        else:
            x = 4
        self.tetromino.updater(x, y=21, shape=shape, orientation='0')

    def probe(self, board, x, y, shape=None, orientation=None):
        if not shape:
            shape = self.tetromino.shape
        if not orientation:
            orientation = self.tetromino.orientation

        coor_list = self.tetromino.shape_dictionary[shape, orientation]
        for num in range(4):
            probing_coor = x + coor_list[2 * num], y + coor_list[2 * num + 1]
            if not board.get(probing_coor):
                return False
            if board.get(probing_coor).status:
                return False
        return True


Key_Event = []


def capture_key(event):
    global Key_Event
    Key_Event.append(event.key)


def main():
    global Key_Event
    red_player = Player('q', 'e', 's', 'w', 'a', 'd', color.red, player='first')
    blue_player = Player('u', 'o', 'k', 'i', 'j', 'l', color.blue, player='second')
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
            player.nat_drop(board)


if __name__ == '__main__':
    main()
