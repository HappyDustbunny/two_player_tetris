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
        self.bag = shuffle(list('IOTSZJL'))
        self.tetramino_pos = {0: [5, 20], 1: [5, 20], 2: [5, 20], 3: [5, 20]}
        self.tetramino = Tetramino(5, 20, 'T', colour=self.color)

    def receive_input(self, board, players, received_inputs):
        action_input = None
        for inp in received_inputs:
            if self.inputs.get(inp):
                action_input = self.inputs[inp]
        if action_input == 's_drop':
            self.nat_drop(board, players)
        elif action_input == 'h_drop':
            self.hard_drop(board)
        elif action_input in (-1, 1):  # -1 and 1 are left and right, respectively
            self.move_tetramino(action_input, board)
        elif action_input in ('turn_ws', 'turn_cw'):
            self.turn_tetramino(action_input, board)

    def nat_drop(self, board):
        droppable = True
        for num in range(4):
            x, y = self.tetramino.boxes[num].pos.x / 10, self.tetramino.boxes[num].pos.y / 10
            if board.get((x, y - 1)):
                print(num, x, y, self.tetramino.color, board.get((x, y - 1)).status)
                if board.get((x, y - 1)).status:
                    droppable = False
            else:
                droppable = False
        if droppable:
            for num in range(4):
                # self.tetramino.boxes[num].pos.y -= 10
                print(num, self.tetramino.boxes[num].pos.x / 10, self.tetramino.boxes[num].pos.y / 10)
                x, y = self.tetramino.boxes[num].pos.x / 10, (self.tetramino.boxes[num].pos.y / 10) - 1
                self.tetramino.updater(x, y)
        else:
            for num in range(4):
                # self.tetramino.boxes[num].color = self.color
                x, y = self.tetramino.boxes[num].pos.x / 10, self.tetramino.boxes[num].pos.y / 10
                colour = self.tetramino.color
                change_cube_state(board, x, y, colour=colour, opacity=1, visible=True)

    def hard_drop(self, board):
        pass

    def move_tetramino(self, action_input, board):
        movable = True
        for num in range(4):
            tet_pos = self.tetramino_pos[num]
            if board.get(tet_pos[0] + action_input, tet_pos[1]).status or \
                    board.get(tet_pos[0] + action_input, tet_pos[1]).status is None:
                movable = False
        if movable:
            for num in range(4):
                self.tetramino_pos[num][0] += action_input

    def turn_tetramino(self, action_input, board):
        pass


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
    scene.center = vector(int(10 * (columns - 1) / 2), int(10 * rows / 2), 0)
    scene.autoscale = False
    red_player.tetramino.shape = 'T'
    blue_player.tetramino.shape = 'Z'
    red_player.tetramino.updater(2, 20, orientation='0')
    blue_player.tetramino.updater(7, 20, orientation='0')
    while True:
        # for y in range(10, 0, -1):
        #     sleep(.2)
        #     red_player.tetramino.updater(2, y, orientation='0')
        for _ in range(20):
            sleep(0.05)
            received_inputs = Key_Event
            for player in players:
                player.receive_input(board, players, received_inputs)
            Key_Event = []
        for player in players:
            player.nat_drop(board)
            sleep(.5)


if __name__ == '__main__':
    main()
