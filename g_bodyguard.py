class Bodyguard:

    def __init__(self):
        self.dict_turtle = {}
        self.dict_galapagos = {}

    def safety_check(self):
        pass

class Turtle:
    def __init__(self, x, y, alpha, g):
        self.x = x
        self.y = y
        self.alpha = alpha

        self.g = g

class Galapagos:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
