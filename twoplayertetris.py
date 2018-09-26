""" Two players, two brick-streams, one board  """

from vpython import box, sleep, vector, scene, color


class MovableBox:
    def __init__(self, up, down, left, right, colour):
        if colour == 'red':
            self.box = box(color=color.red)
        elif colour == 'blue':
            self.box = box(color=color.blue)
        else:
            self.box = box()
        self.inputs = {up: vector(0, 1, 0), down: vector(0, -1, 0), left: vector(-1, 0, 0), right: vector(1, 0, 0)}

    def receive_input(self, received_inputs):
        action_input = None
        for inp in received_inputs:
            if self.inputs.get(inp):
                action_input = inp
        if action_input:
            self.box.pos += self.inputs[action_input]


Key_Event = []


def capture_key(event):
    global Key_Event
    Key_Event.append(event.key)


def main():
    global Key_Event
    red_box = MovableBox('w', 's', 'a', 'd', 'red')
    blue_box = MovableBox('i', 'k', 'j', 'l', 'blue')
    boxes = (red_box, blue_box)
    scene.bind('keydown', capture_key)
    while True:
        for _ in range(20):
            sleep(0.05)
            key = Key_Event
            for colored_box in boxes:
                colored_box.receive_input(key)
            Key_Event = []
            key = None
        # once per second, move the block down.


if __name__ == '__main__':
    main()
