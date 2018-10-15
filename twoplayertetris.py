""" Two Player Tetris  """

from vpython import color, scene, sleep, vector

from random import shuffle

from graphics import change_cube_state, draw_board, Tetramino


class Player:
    def __init__(self, turn_widdershins, turn_clockwise, soft_drop, hard_drop, left, right, colour):
        """ Inputs define which keys to use: Player(a,s,w,d,...) """
        self.inputs = {turn_widdershins: 'turn_ws', turn_clockwise: 'turn_cw',
                       soft_drop: 's_drop', hard_drop: 'h_drop', left: -1, right: 1}
        self.bag = list('IOTSZJL')
        shuffle(self.bag)
        self.tetramino = Tetramino(5, 20, 'T', colour=colour)

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
            self.move_tetramino(action_input, board)
        elif action_input in ('turn_ws', 'turn_cw'):
            self.turn_tetramino(action_input, board)

    def move_tetramino(self, action_input, board):
        if self.probe(board, self.tetramino.x_pos + action_input, self.tetramino.y_pos):
            self.tetramino.updater(self.tetramino.x_pos + action_input, self.tetramino.y_pos)

    def turn_tetramino(self, action_input, board):
        # TODO: If a tetramino tries to turn next to a wall,
        # TODO: it's supposed to be allowed to move away from the wall to be able to turn.

        # TODO: The turning isn't up to the official standards for how tetraminoes are supposed to turn.
        if action_input == 'turn_ws':
            if self.tetramino.orientation == '0':
                if self.probe(board, self.tetramino.x_pos, self.tetramino.y_pos, orientation='3'):
                    self.tetramino.updater(self.tetramino.x_pos, self.tetramino.y_pos, orientation='3')
            else:
                new_ori = str(int(self.tetramino.orientation) - 1)
                if self.probe(board, self.tetramino.x_pos, self.tetramino.y_pos, orientation=new_ori):
                    self.tetramino.updater(self.tetramino.x_pos, self.tetramino.y_pos, orientation=new_ori)
        if action_input == 'turn_cw':
            if self.tetramino.orientation == '3':
                if self.probe(board, self.tetramino.x_pos, self.tetramino.y_pos, orientation='0'):
                    self.tetramino.updater(self.tetramino.x_pos, self.tetramino.y_pos, orientation='0')
            else:
                new_ori = str(int(self.tetramino.orientation) + 1)
                if self.probe(board, self.tetramino.x_pos, self.tetramino.y_pos, orientation=new_ori):
                    self.tetramino.updater(self.tetramino.x_pos, self.tetramino.y_pos, orientation=new_ori)

    def nat_drop(self, board):
        if self.probe(board, self.tetramino.x_pos, self.tetramino.y_pos - 1):
            self.tetramino.updater(self.tetramino.x_pos, self.tetramino.y_pos - 1)
        else:
            self.landing_procedure(board)

    def hard_drop(self, board):
        for y in range(0, self.tetramino.y_pos):
            if self.probe(board, self.tetramino.x_pos, y=y):
                self.tetramino.updater(self.tetramino.x_pos, y=y)
                # TODO: Decide if landing_procedure should also happen here.
                return

    def landing_procedure(self, board):
        for num in range(4):
            x, y = self.tetramino.boxes[num].pos.x, self.tetramino.boxes[num].pos.y
            colour = self.tetramino.color
            change_cube_state(board, x, y, colour=colour, opacity=1, status=True, visible=True)
        if not self.bag:
            self.bag = list('IOTSZJL')
            shuffle(self.bag)
        shape = self.bag.pop(0)
        if shape == 'I':
            x = 3
        else:
            x = 4
        self.tetramino.updater(x, y=21, shape=shape, orientation='0')

    def probe(self, board, x, y, shape=None, orientation=None):
        if not shape:
            shape = self.tetramino.shape
        if not orientation:
            orientation = self.tetramino.orientation

        coor_list = self.tetramino.shape_dictionary[shape, orientation]
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
    red_player = Player('q', 'e', 's', 'w', 'a', 'd', color.red)
    blue_player = Player('u', 'o', 'k', 'i', 'j', 'l', color.blue)
    players = [red_player, blue_player]
    scene.bind('keydown', capture_key)
    columns, rows = 10, 24
    board = draw_board(columns, rows)
    scene.center = vector(int(1 * (columns - 1) / 2), int(1 * rows / 2), 0)
    scene.autoscale = False
    red_player.tetramino.updater(2, 20, shape='T', orientation='0')
    blue_player.tetramino.updater(7, 20, shape='O', orientation='1')

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
