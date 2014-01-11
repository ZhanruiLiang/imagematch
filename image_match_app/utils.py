from __future__ import print_function

class ProgressBar:
    def __init__(self, total, freq=1000):
        self.total = total
        self.cnt = 0
        self.printFreq = freq

    def update(self):
        self.cnt += 1
        if self.cnt == self.total or self.cnt % self.printFreq == 0:
            bar = '{:60s} '.format('|' * (60 * self.cnt // self.total))
            print('\rprogress: [{}] {}/{} ({:.2f})%'.format(
                bar, self.cnt, self.total, 100 * self.cnt / self.total), end='')
