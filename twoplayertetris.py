""" Two Player Tetris  """

from vpython import color, scene, sleep, vector

from random import shuffle

from graphics import change_cube_state, draw_board, Tetramino


# class MovableBox:
#     def __init__(self, up, down, left, right, colour):
#         self.box = box(color=colour)
#         else:
#             self.box = box()
#         self.inputs = {up: vector(0, 1, 0), down: vector(0, -1, 0), left: vector(-1, 0, 0), right: vector(1, 0, 0)}
#
#     def receive_input(self, received_inputs):
#         action_input = None
#         for inp in received_inputs:
#             if self.inputs.get(inp):
#                 action_input = inp
#         if action_input:
#             self.box.pos += self.inputs[action_input]


class Player:
    def __init__(self, turn_widdershins, turn_clockwise, soft_drop, hard_drop, left, right, colour):
        self.color = colour
        self.inputs = {turn_widdershins: 'turn_ws', turn_clockwise: 'turn_cw',
                       soft_drop: 's_drop', hard_drop: 'h_drop', left: -1, right: 1}
        self.bag = list('IOTSZJL')
        shuffle(self.bag)
        # self.tetramino_pos = {0: [5, 20], 1: [5, 20], 2: [5, 20], 3: [5, 20]}
        self.tetramino = Tetramino(5, 20, 'T', colour=self.color)

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

    def nat_drop(self, board):
        droppable = True
        for num in range(4):
            x, y = self.tetramino.boxes[num].pos.x, self.tetramino.boxes[num].pos.y
            if not board.get((x, y - 1)):
                droppable = False
                continue
            print(num, x, y, self.tetramino.color, board.get((x, y - 1)).status)
            if board.get((x, y - 1)).status:
                droppable = False
        if droppable:
            self.tetramino.updater(self.tetramino.x_pos, self.tetramino.y_pos - 1)
        else:
            self.landing_procedure(board)

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
        self.tetramino.updater(x, 21, shape=shape, orientation='0')

    def hard_drop(self, board):
        pass

    def move_tetramino(self, action_input, board):
        movable = True
        for num in range(4):
            x, y = self.tetramino.boxes[num].pos.x, self.tetramino.boxes[num].pos.y
            if not board.get((x + action_input, y)):
                movable = False
                continue
            if board.get((x + action_input, y)).status:
                movable = False
        if movable:
            self.tetramino.updater(self.tetramino.x_pos + action_input, self.tetramino.y_pos)

    def turn_tetramino(self, action_input, board):
        if action_input == 'turn_ws':
            if self.tetramino.orientation == '0':
                self.tetramino.updater(self.tetramino.x_pos, self.tetramino.y_pos, orientation='3')
            else:
                new_ori = str(int(self.tetramino.orientation) - 1)
                self.tetramino.updater(self.tetramino.x_pos, self.tetramino.y_pos, orientation=new_ori)
        if action_input == 'turn_cw':
            if self.tetramino.orientation == '3':
                self.tetramino.updater(self.tetramino.x_pos, self.tetramino.y_pos, orientation='0')
            else:
                new_ori = str(int(self.tetramino.orientation) + 1)
                self.tetramino.updater(self.tetramino.x_pos, self.tetramino.y_pos, orientation=new_ori)



Key_Event = []


def capture_key(event):
    global Key_Event
    Key_Event.append(event.key)


def main():
    global Key_Event
    # board_status = {(x, y): False for x in list(range(10)) for y in list(range(24))}
    red_player = Player('q', 'e', 's', 'w', 'a', 'd', color.red)
    blue_player = Player('u', 'o', 'k', 'i', 'j', 'l', color.blue)
    players = [red_player, blue_player]
    scene.bind('keydown', capture_key)
    columns, rows = 10, 24
    board = draw_board(columns, rows)
    scene.center = vector(int(1 * (columns - 1) / 2), int(1 * rows / 2), 0)
    scene.autoscale = False
    red_player.tetramino.updater(2, 20, orientation='0', shape='T')
    blue_player.tetramino.updater(7, 20, orientation='1', shape='O')

    while True:
        # for y in range(10, 0, -1):
        #     sleep(.2)
        #     red_player.tetramino.updater(2, y, orientation='0')
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
