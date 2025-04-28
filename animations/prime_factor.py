import math
import time

# — primality tests
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

# — largest-prime-factor functions
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

# — dual‐algorithm progression
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

        self.bar_naive = self.ax.barh(2, 0, height=0.4, color='blue', alpha=0.6)[0]
        self.bar_opt   = self.ax.barh(1, 0, height=0.4, color='red',  alpha=0.6)[0]

        self.txt_naive = self.ax.text(self.n*0.5, 2.3, 'Naive max PF: –', ha='center')
        self.txt_opt   = self.ax.text(self.n*0.5, 1.3, 'Opt  max PF: –', ha='center')

    def update(self):
        cont = False

        # — naive scans up
        if self.i <= self.n // 2:
            cont = True
            if self.n % self.i == 0 and is_prime_naive(self.i):
                self.max_naive = self.i
                self.txt_naive.set_text(f'Naive max PF: {self.max_naive}')
            self.bar_naive.set_width(self.i)
            self.i += 1

        # — optimized scans down until it finds a prime
        if not self.opt_done and self.j >= 2:
            cont = True
            if self.n % self.j == 0:
                cp = self.n // self.j
                if is_prime_opt(cp):
                    self.max_opt = cp
                    self.txt_opt.set_text(f'Opt  max PF: {self.max_opt}')
                    self.opt_done = True
                elif is_prime_opt(self.j):
                    self.max_opt = self.j
                    self.txt_opt.set_text(f'Opt  max PF: {self.max_opt}')
                    self.opt_done = True
                # else: keep scanning
            self.bar_opt.set_width(self.j)
            self.j -= 1

        return cont

# — static runtime comparison w/ hover
class PrimeFactorPerformance:
    def __init__(self, sizes, ax):
        self.sizes = sizes
        self.ax = ax
        self.fig = ax.figure
        self.times_naive = []
        self.times_opt = []
        self._compute_times()
        self._plot()
        self._connect()

    def _compute_times(self):
        for n in self.sizes:
            t0 = time.time(); naive_lpf(n); t1 = time.time()
            self.times_naive.append(t1 - t0)
            t2 = time.time(); optimized_lpf(n); t3 = time.time()
            self.times_opt.append(t3 - t2)

    def _plot(self):
        self.ax.clear()
        self.ax.plot(self.sizes, self.times_naive, 'o-', label='Naive (O(n²))')
        self.ax.plot(self.sizes, self.times_opt,   's-', label='Optimized (O(log n))')
        self.ax.set_xscale('log'); self.ax.set_yscale('log')
        self.ax.set_title('LPF Runtime Comparison', fontweight='bold')
        self.ax.set_xlabel('n'); self.ax.set_ylabel('Time (s)')
        self.ax.legend()

        # invisible scatters for tooltips
        self.scat_naive = self.ax.scatter(self.sizes, self.times_naive, s=50, color='blue',  alpha=0)
        self.scat_opt   = self.ax.scatter(self.sizes, self.times_opt,   s=50, color='red',   alpha=0)

    def _connect(self):
        self.annot = self.ax.annotate(
            "", xy=(0,0), xytext=(10,10), textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->")
        )
        self.annot.set_visible(False)
        self.fig.canvas.mpl_connect("motion_notify_event", self._hover)

    def _hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            c1, i1 = self.scat_naive.contains(event)
            c2, i2 = self.scat_opt.contains(event)
            if c1:
                idx = i1["ind"][0]
                x, y = self.sizes[idx], self.times_naive[idx]
            elif c2:
                idx = i2["ind"][0]
                x, y = self.sizes[idx], self.times_opt[idx]
            else:
                if vis:
                    self.annot.set_visible(False); self.fig.canvas.draw_idle()
                return
            xs = f"{x:.3e}" if x >= 1e5 else str(x)
            ys = f"{y:.3e} s"
            self.annot.xy = (x, y)
            self.annot.set_text(f"{xs}\n{ys}")
            self.annot.set_visible(True)
            self.fig.canvas.draw_idle()
        else:
            if vis:
                self.annot.set_visible(False); self.fig.canvas.draw_idle()

    def update(self):
        return False
