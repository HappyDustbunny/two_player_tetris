""" """

from vpython import box, sleep, vector, scene, color

from random import shuffle


# class MovableBox:
#     def __init__(self, up, down, left, right, colour):
#         if colour == 'red':
#             self.box = box(color=color.red)
#         elif colour == 'blue':
#             self.box = box(color=color.blue)
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
                       soft_drop: 's_drop', hard_drop:'h_drop', left: 'left', right: 'right'}
        self.tetramino_list = list('IOTSZJL')
        self.tetramino_bag = shuffle(self.tetramino_list)

    def receive_input(self, received_inputs):
        action_input = None
        for inp in received_inputs:
            if self.inputs.get(inp):
                action_input = self.inputs[inp]
        if action_input in ('left', 'right', 's_drop', 'h_drop'):
            self.move_tetramino(action_input)
        elif action_input in ('turn_ws', 'turn_cw'):
            self.turn_tetramino(action_input)

    def move_tetramino(self, action_input):
        pass

    def turn_tetramino(self, action_input):
        pass


Key_Event = []


def capture_key(event):
    global Key_Event
    Key_Event.append(event.key)


def main():
    global Key_Event
    red_player = Player('q', 'e', 's', 'w', 'a', 'd', 'red')
    blue_player = Player('u', 'o', 'k', 'i', 'j', 'l', 'blue')
    players = [red_player, blue_player]
    scene.bind('keydown', capture_key)
    while True:
        for _ in range(20):
            sleep(0.05)
            key = Key_Event
            for player in players:
                player.receive_input(key)
            Key_Event = []
            key = None
        # once per second, move the block down.


if __name__ == '__main__':
    main()
