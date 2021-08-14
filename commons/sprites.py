class Sprite:
    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.horizontal_center = x + w / 2


class Rex(Sprite):
    pass


class Cactus(Sprite):
    pass
