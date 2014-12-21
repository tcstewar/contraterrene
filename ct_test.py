import numpy as np

def sample_to_sum(target, sd, count):
    s = np.random.randn(count) * sd / np.sqrt(count)
    s += (target - sum(s)) / count
    return s

def int_sample_to_sum(target, sd, count):
    s = sample_to_sum(target, sd, count)
    result = (np.cumsum(s) + np.random.rand()).astype(int)
    result[1:] = np.diff(result)
    return result


class Forest(object):
    def __init__(self):
        self.predator = int(np.random.normal(100, 20))
        self.prey = int(np.random.normal(400, 20))

    def update(self):
        x = self.prey
        y = self.predator
        dt = 0.001
        dx = dt * (50 * x - 1.6 * x * y)# + (300 - x) * 1)
        dy = dt * (-25 * y + 0.1 * x * y)

        dx_sd = x * 0.01
        dy_sd = y * 0.01
        int_dx = int(dx + np.random.randn() * dx_sd)
        int_dy = int(dy + np.random.randn() * dy_sd)

        self.prey += int_dx
        self.predator += int_dy
        if self.prey < 0:
            self.prey = 0
        if self.predator < 0:
            self.predator = 0

    def flow(self, other):
        rate = 0.001
        prey_out = np.random.binomial(self.prey, rate)
        pred_out = np.random.binomial(self.predator, rate)
        prey_in = np.random.binomial(other.prey, rate)
        pred_in = np.random.binomial(other.predator, rate)

        self.prey -= prey_out
        self.prey += prey_in
        other.prey += prey_out
        other.prey -= prey_in

        self.predator -= pred_out
        self.predator += pred_in
        other.predator += pred_out
        other.predator -= pred_in


if __name__ == '__main__':
    N = 4
    forest = [Forest() for i in range(N)]

    for f in forest:
        f.x = []
        f.y = []
    for i in range(10000):
        for f in forest:
            f.update()
        for i in range(len(forest)-1):
            forest[i].flow(forest[i+1])
        for f in forest:
            f.x.append(f.prey)
            f.y.append(f.predator)

    import pylab
    for i in range(N):
        pylab.subplot(N,1, i+1)
        pylab.plot(forest[i].x)
        pylab.plot(forest[i].y)
    pylab.figure()
    pylab.plot(np.sum([f.x for f in forest], axis=0))
    pylab.plot(np.sum([f.y for f in forest], axis=0))
    pylab.show()




