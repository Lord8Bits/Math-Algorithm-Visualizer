import math
import time

# —— primality tests
def is_prime_naive(m):
    if m <= 1:
        return False
    for j in range(2, int(math.isqrt(m)) + 1):
        if m % j == 0:
            return False
    return True

def is_prime_opt(m):
    if m <= 1:
        return False
    if m <= 3:
        return True
    if m % 2 == 0 or m % 3 == 0:
        return False
    limit = int(math.isqrt(m))
    i = 5
    while i <= limit:
        if m % i == 0 or m % (i + 2) == 0:
            return False
        i += 6
    return True

# —— largest prime-factor routines
def naive_lpf(n):
    max_p = None
    for i in range(2, n // 2 + 1):
        if n % i == 0 and is_prime_naive(i):
            max_p = i
    if max_p is None and n > 1:
        return n
    return max_p

def optimized_lpf(n):
    for i in range(int(math.isqrt(n)), 1, -1):
        if n % i == 0:
            cp = n // i
            if is_prime_opt(cp):
                return cp
            if is_prime_opt(i):
                return i
    return None

# —— dual-algorithm progression
class DualPrimeFactorProgression:
    def __init__(self, n, ax):
        self.n = n
        self.ax = ax
        self.i = 2
        self.j = int(math.isqrt(n))
        self.max_naive = None
        self.max_opt = None
        self.opt_done = False
        self._setup()

    def _setup(self):
        self.ax.clear()
        self.ax.set_xlim(0, self.n)
        self.ax.set_ylim(0.5, 2.5)
        self.ax.set_title(f'Dual LPF Progression – n={self.n}', fontweight='bold')
        self.ax.set_xlabel('Tested Divisor')
        self.ax.set_yticks([])

        # bars at y=2 (naive) and y=1 (optimized)
        self.bar_naive = self.ax.barh(2, 0, height=0.4, color='blue', alpha=0.6)[0]
        self.bar_opt   = self.ax.barh(1, 0, height=0.4, color='red',  alpha=0.6)[0]

        # text labels
        self.txt_naive = self.ax.text(self.n * 0.5, 2.3, 'Naive max PF: –', ha='center')
        self.txt_opt   = self.ax.text(self.n * 0.5, 1.3, 'Opt  max PF: –', ha='center')

    def update(self):
        cont = False

        # naive scans up from 2 → n/2
        if self.i <= self.n // 2:
            cont = True
            if self.n % self.i == 0 and is_prime_naive(self.i):
                self.max_naive = self.i
                self.txt_naive.set_text(f'Naive max PF: {self.max_naive}')
            self.bar_naive.set_width(self.i)
            self.i += 1

        # optimized scans down from √n → 2, stops at first factor
        if not self.opt_done and self.j >= 2:
            cont = True
            if self.n % self.j == 0:
                cp = self.n // self.j
                if is_prime_opt(cp):
                    self.max_opt = cp
                elif is_prime_opt(self.j):
                    self.max_opt = self.j
                self.txt_opt.set_text(f'Opt  max PF: {self.max_opt}')
                self.opt_done = True
            self.bar_opt.set_width(self.j)
            self.j -= 1

        return cont

# —— static runtime comparison
class PrimeFactorPerformance:
    def __init__(self, sizes, ax):
        self.sizes = sizes
        self.ax = ax
        self._plot()

    def _plot(self):
        times_naive = []
        times_opt   = []

        for n in self.sizes:
            t0 = time.time()
            naive_lpf(n)
            t1 = time.time()
            times_naive.append(t1 - t0)

            t2 = time.time()
            optimized_lpf(n)
            t3 = time.time()
            times_opt.append(t3 - t2)

        self.ax.clear()
        self.ax.plot(self.sizes, times_naive, 'o-', label='Naive (O(n²))')
        self.ax.plot(self.sizes, times_opt,   's-', label='Optimized (O(log n))')
        self.ax.set_xscale('log')
        self.ax.set_yscale('log')
        self.ax.set_title('LPF Runtime Comparison', fontweight='bold')
        self.ax.set_xlabel('n')
        self.ax.set_ylabel('Time (s)')
        self.ax.legend()

    def update(self):
        return False
