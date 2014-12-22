import numpy as np

class Agent(object):
    def __init__(self, world, x=None, y=None):
        if x is None:
            x = np.random.randint(world.width)
        if y is None:
            y = np.random.randint(world.height)
        self.x = x
        self.y = y
        self.world = world

    def move_randomly(self):
        self.x += np.random.randint(3) - 1
        self.y += np.random.randint(3) - 1


class Predator(Agent):
    def __init__(self, world, x=None, y=None, hunger=None):
        if hunger is None:
            hunger = np.random.randint(40)
        self.hunger = hunger
        super(Predator, self).__init__(world, x, y)

class Prey(Agent):
    pass

class Event(object):
    def __init__(self, obj=None):
        self.obj = obj

class GoNorth(Event):
    def resolve(self, world):
        if isinstance(self.obj, Predator):
            pred = Predator(self, x=self.obj.x, y=world.height - 1)
            world.pred.append(pred)
        elif isinstance(self.obj, Prey):
            prey = Prey(self, x=self.obj.x, y=world.height - 1)
            world.prey.append(prey)

class GoSouth(Event):
    def resolve(self, world):
        if isinstance(self.obj, Predator):
            pred = Predator(self, x=self.obj.x, y=0)
            world.pred.append(pred)
        elif isinstance(self.obj, Prey):
            prey = Prey(self, x=self.obj.x, y=0)
            world.prey.append(prey)

class GoWest(Event):
    def resolve(self, world):
        if isinstance(self.obj, Predator):
            pred = Predator(self, x=world.width - 1, y=self.obj.y)
            world.pred.append(pred)
        elif isinstance(self.obj, Prey):
            prey = Prey(self, x=world.width - 1, y=self.obj.y)
            world.prey.append(prey)

class GoEast(Event):
    def resolve(self, world):
        if isinstance(self.obj, Predator):
            pred = Predator(self, x=0, y=self.obj.y)
            world.pred.append(pred)
        elif isinstance(self.obj, Prey):
            prey = Prey(self, x=0, y=self.obj.y)
            world.prey.append(prey)

class PPGrid(object):
    def __init__(self, width, height, pred=None, prey=None):
        if pred is None:
            pred = int(np.random.normal(100, 20))
        if prey is None:
            prey = int(np.random.normal(400, 20))

        self.width = width
        self.height = height

        self.pred = [Predator(self) for i in range(pred)]
        self.prey = [Prey(self) for i in range(prey)]

    def step(self, events):
        for e in events:
            e.resolve(self)

        events = []
        pred_birth = 0
        # prey birth
        p = np.random.rand(len(self.prey))
        for i, prey in enumerate(self.prey[:]):
            if p[i] < 0.01:
                self.prey.append(Prey(self, x=prey.x, y=prey.y))
                pred_birth += 1

        eat = 0
        pred_death = 0
        pred_birth = 0
        for pred in self.pred:
            for prey in self.prey:
                if prey.x == pred.x and prey.y == pred.y:
                    eat += 1
                    pred.hunger = 40
                    self.prey.remove(prey)
                    if np.random.random() < 0.01:
                        self.pred.append(Predator(self, x=pred.x, y=pred.y))
                        pred_birth += 1
            pred.hunger -= 1
            if pred.hunger <= 0:
                pred_death += 1
                self.pred.remove(pred)

        for p in self.pred:
            p.move_randomly()
            if p.x < 0:
                events.append(GoWest(p))
                self.pred.remove(p)
            elif p.y < 0:
                events.append(GoNorth(p))
                self.pred.remove(p)
            elif p.x >= self.width:
                events.append(GoEast(p))
                self.pred.remove(p)
            elif p.y >= self.height:
                events.append(GoSouth(p))
                self.pred.remove(p)

        for p in self.prey:
            p.move_randomly()
            if p.x < 0:
                events.append(GoWest(p))
                self.prey.remove(p)
            elif p.y < 0:
                events.append(GoNorth(p))
                self.prey.remove(p)
            elif p.x >= self.width:
                events.append(GoEast(p))
                self.prey.remove(p)
            elif p.y >= self.height:
                events.append(GoSouth(p))
                self.prey.remove(p)


if __name__ == '__main__':
    world = PPGrid(50, 50)
    x = []
    y = []
    for i in range(5000):
        x.append(len(world.prey))
        y.append(len(world.pred))
        print i, len(world.prey), len(world.pred)
        world.step(events=[GoNorth(Predator(None, x=np.random.randint(world.width), y=0))])

    import pylab
    pylab.plot(x)
    pylab.plot(y)
    pylab.show()




