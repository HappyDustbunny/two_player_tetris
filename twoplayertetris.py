""" Two players, two brick-streams, one board """

from vpython import box, sleep, vector


def capture_key(event):
    """ Capture keyboard interrupt and choose new direction and new orientation """
    global key_event
    key_event = event.key

def main():
    global key_event
    scene.bind('keydown', capture_key)
    while True:
        key = key_event
        box()


if __name__ == '__main__':
    main()
