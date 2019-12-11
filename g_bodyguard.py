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
            print("In galapagos")
        else:
            print("Out galapagos")

        if self._is_colliding(turtle):
            print("Is colliding")
        else:
            print("No collision")

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

    def __init__(self, x, y, alpha, g):
        super(Turtle, self).__init__()
        self.x = x
        self.y = y
        self.alpha = alpha

        self.g = g

    def update_pos(self, pos):
        self.x += pos
        self.notify_observer()

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

    t.update_pos(80)

    t2 = Turtle(0, 0, 30, 'g1')
    b.add_turtle("t2", t2)

    t2.update_pos(105)
