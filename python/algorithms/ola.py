import time

from python.lattice import generate_lattice


class OLA:
    MAX_TIME = 30

    def __init__(self, k_anonymity):
        self.k = k_anonymity
        self.results = []
        self.tagged = {}
        self.start = None

    def run(self):
        self.start = time.time()
        bottom = self.k.lower_bounds
        top = self.k.upper_bounds
        self._kmin(bottom, top)
        return self.results

    def _kmin(self, bottom, top):
        if time.time() - self.start > self.MAX_TIME:
            return

        lattice = generate_lattice(bottom, top)
        max_h = max(lattice.keys())

        if max_h > 1:
            h = max_h // 2
            for node in lattice[h]:
                if self._is_tagged(node.gen, True):
                    self._kmin(bottom, list(node.gen))
                elif self._is_tagged(node.gen, False):
                    self._kmin(list(node.gen), top)
                elif self.k.is_k_anonymous(node.gen, 2, 0.0):
                    self._tag(node.gen, True)
                    self._kmin(bottom, list(node.gen))
                else:
                    self._tag(node.gen, False)
                    self._kmin(list(node.gen), top)
        else:
            chosen = top if not self.k.is_k_anonymous(bottom, 2, 0.0) else bottom
            if chosen not in self.results:
                self.results.append(chosen)

    def _tag(self, gen, value):
        self.tagged[tuple(gen)] = value

    def _is_tagged(self, gen, value):
        return self.tagged.get(tuple(gen)) is value