import numpy as np

class PredPrey(object):
    def __init__(self, pred=None, prey=None):
        if pred is None:
            pred = int(np.random.normal(100, 20))
        if prey is None:
            prey = int(np.random.normal(400, 20))
        self.pred = pred
        self.prey = prey
        self.link = {}

    def flow_in(self, pred, prey):
        self.prey += prey
        self.pred += pred

    def step(self):
        prey_birth = np.random.binomial(self.prey, 0.1)
        eat = np.random.binomial(self.pred * self.prey, 0.002)
        if eat > self.prey:
            eat = self.prey

        starving = self.pred - 4 * eat
        if starving > 0:
            pred_death = np.random.binomial(starving, 0.05)
        else:
            pred_death = 0

        pred_birth = np.random.binomial(eat, 0.01)

        self.pred += pred_birth
        self.prey += prey_birth
        self.prey -= eat
        self.pred -= pred_death

        rate = 0.1
        for link in self.link.values():
            prey_out = np.random.binomial(self.prey, rate)
            pred_out = np.random.binomial(self.pred, rate)
            self.prey -= prey_out
            self.pred -= pred_out
            link.flow_in(pred=pred_out, prey=prey_out)


if __name__ == '__main__':
    N = 100
    forest = [PredPrey() for i in range(N)]

    for i in range(N-1):
        forest[i].link['east'] = forest[i + 1]
        forest[i - 1].link['west'] = forest[i]

    for f in forest:
        f.x = []
        f.y = []
    for i in range(1000):
        for f in forest:
            f.step()
        for f in forest:
            f.x.append(f.prey)
            f.y.append(f.pred)

    import pylab
    '''
    for i in range(N):
        pylab.subplot(N,1, i+1)
        pylab.plot(forest[i].x)
        pylab.plot(forest[i].y)
    pylab.figure()
    '''
    pylab.plot(np.sum([f.x for f in forest], axis=0))
    pylab.plot(np.sum([f.y for f in forest], axis=0))
    pylab.show()




