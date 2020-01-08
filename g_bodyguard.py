from math import cos, sin, pi
import logging

logger = logging.getLogger('compiler')

class Bodyguard:

    def __init__(self):
        self.dict_turtle = {}
        self.dict_galapagos = {}

    def add_galapagos(self, galapagos_name, galapagos):
        self.dict_galapagos[galapagos_name] = galapagos

    def add_turtle(self, turtle_name, turtle):
        self.dict_turtle[turtle_name] = turtle
        self.dict_turtle[turtle_name].add_observer(self)

    def safety_check(self, turtle):
        galapagos = self.dict_galapagos[turtle.g]

        if self._is_in_galapagos(galapagos, turtle):
            logger.debug(f"Safe: Turtle '{turtle.name}' stayed inside galapagos")
        else:
            logger.debug("Error: out of galapagos")
            raise Exception(f"Error: Turtle '{turtle.name}' (x: {int(turtle.x)}; y: {int(turtle.y)}) went out of galapagos {turtle.g}")

        if self._is_colliding(turtle):
            logger.debug("Error: Collision between turtles")
            raise Exception(f"Error: turtle '{turtle.name}' (x: {int(turtle.x)}; y: {int(turtle.y)}) collided")
        else:
            logger.debug("No collision")

    def _is_in_galapagos(self, galapagos, turtle):
        return turtle.x >= galapagos.x and turtle.x <= galapagos.x + galapagos.width \
            and turtle.y >= galapagos.y and turtle.y <= galapagos.y + galapagos.height

    def _is_colliding(self, turtle):
        t_xrange = [turtle.x + 10, turtle.x - 10]
        t_yrange = [turtle.y + 10, turtle.y - 10]
        collision_check = lambda t: t.x in t_xrange or t.y in t_yrange

        return len(list(filter(collision_check, self.dict_turtle.values()))) > 0

class Observable:

    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observer(self):
        for observer in self.observers:
            observer.safety_check(self)

class Turtle(Observable):

    def __init__(self, name, g, x, y, alpha):
        super(Turtle, self).__init__()
        self.name = name
        self.g = g
        self.x = x
        self.y = y
        self.alpha = alpha

    def move_straight(self, distance):
        self.x += distance * cos(self.alpha * (pi/180))
        self.y += distance * sin(self.alpha * (pi/180))
        self.notify_observer()

    def move_back(self, distance):
        self.move_straight(-distance)
        self.notify_observer()

    def turn_right(self, angle):
        self.alpha -= -angle * (pi/180)

    def turn_left(self, angle):
        self.alpha += -angle * (pi/180)


MIN_X = 0
MIX_Y = 0
MAX_WIDTH = 1000
MAX_HEIGHT = 500

class Galapagos:

    def __init__(self, x, y, width, height):
        '''
        if x + width <= MAX_WIDTH and y + height <= MAX_HEIGHT and x >= 0 and y >= 0 and width > 0 and height > 0:
            self.x = x
            self.y = y
            self.width = width
            self.height = height
        else:
            raise Exception("dimensions are wrong. chose anoter ones")
        '''
        self.x = x
        self.y = y
        self.width = width
        self.height = height
