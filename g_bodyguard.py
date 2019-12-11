from math import cos, sin, pi

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
        print("Should check safety")
        galapagos = self.dict_galapagos[turtle.g]
        if self._is_out_galapagos(galapagos, turtle):
            print("Out of galapagos")
        else:
            print("Is safe")

    def _is_out_galapagos(self, galapagos, turtle):
        return turtle.x < galapagos.x or turtle.x > galapagos.x + galapagos.width \
            or turtle.y < galapagos.y or turtle.y > galapagos.y + galapagos.height

class Observable:

    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observer(self):
        for observer in self.observers:
            observer.safety_check(self)

class Turtle(Observable):

    def __init__(self, x, y, alpha, g):
        super(Turtle, self).__init__()
        self.x = x
        self.y = y
        self.alpha = alpha

        self.g = g

    def update_pos(self, pos):
        self.x += pos
        self.notify_observer()
    
    def move_straight(self, distance):
        self.x += distance * cos(self.alpha)
        self.y += distance * sin(self.alpha)
    
    def move_back(self, distance):
        self.move_straight(-distance)
    
    def turn_right(self, angle):
        self.alpha += -angle * (pi/180)
    
    def turn_left(self, angle):
        self.alpha -= -angle * (pi/180)


class Galapagos:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

if __name__ == "__main__":
    b = Bodyguard()

    g = Galapagos(0, 0, 100, 100)
    b.add_galapagos('g1', g)

    t = Turtle(0, 0, 30, 'g1')
    b.add_turtle("t1", t)

    t.update_pos(100)
    t.update_pos(1000)
