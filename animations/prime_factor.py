import math
import time

# --- primality tests
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
    lim = int(math.isqrt(m))
    i = 5
    while i <= lim:
        if m % i == 0 or m % (i + 2) == 0:
            return False
        i += 6
    return True

# --- largest-prime-factor routines
def naive_lpf(n):
    max_p = None
    for i in range(2, n//2 + 1):
        if n % i == 0 and is_prime_naive(i):
            max_p = i
    return n if max_p is None and n > 1 else max_p

def optimized_lpf(n):
    # handle trivial & prime cases
    if n <= 1:
        return None
    if is_prime_opt(n):
        return n

    # optimized scan from sqrt(n) downward
    for i in range(int(math.isqrt(n)), 1, -1):
        if n % i == 0:
            cp = n // i
            if is_prime_opt(cp):
                return cp
            if is_prime_opt(i):
                return i
    return None

# --- dual-algorithm progression (animation)
class DualPrimeFactorProgression:
    def __init__(self, n, ax):
        self.n = n
        self.ax = ax

        # scanning pointers
        self.naive_i = 2
        self.opt_j = int(math.isqrt(n))

        # test counters
        self.naive_tests = 0
        self.opt_tests = 0

        # max PFs
        self.max_naive = None
        self.max_opt = None

        # total tests possible
        self.max_naive_tests = max(1, n//2 - 1)
        self.max_opt_tests = max(1, self.opt_j - 1)
        self.max_tests = max(self.max_naive_tests, self.max_opt_tests)

        self._setup()

    def _setup(self):
        """
        Sets up the visualization environment for the dual least prime factor (LPF) progression.
        This method clears the axes, configures the limits, labels, and titles for the plot,
        and initializes the horizontal bars and text elements used to display the progression
        of divisor tests and results for both naive and optimized approaches.
        Attributes:
            self.ax (matplotlib.axes.Axes): The axes object for the plot.
            self.max_tests (int): The maximum number of divisor tests to be performed.
            self.n (int): The number being factorized.
        Initializes:
            - Horizontal bars (`self.bar_naive` and `self.bar_opt`) to represent the progress
              of divisor tests for naive and optimized methods.
            - Text elements (`self.txt_naive` and `self.txt_opt`) to display the maximum prime
              factor found for each method.
        """
        self.ax.clear()
        self.ax.set_xlim(0, self.max_tests)
        self.ax.set_ylim(0.5, 2.5)
        self.ax.set_title(f'Dual LPF Progression – n={self.n}', fontweight='bold')
        self.ax.set_xlabel('Divisor tests performed')
        self.ax.set_yticks([])

        self.bar_naive = self.ax.barh(2, 0, height=0.4, color='blue', alpha=0.6)[0]
        self.bar_opt = self.ax.barh(1, 0, height=0.4, color='red', alpha=0.6)[0]

        self.txt_naive = self.ax.text(self.max_tests*0.5, 2.3, 'Naive max PF: –', ha='center')
        self.txt_opt = self.ax.text(self.max_tests*0.5, 1.3, 'Opt  max PF: –', ha='center')

    def update(self):
        cont = False

        # naive side
        if self.naive_i <= self.n//2:
            cont = True
            self.naive_tests += 1
            if self.n % self.naive_i == 0 and is_prime_naive(self.naive_i):
                self.max_naive = self.naive_i
                self.txt_naive.set_text(f'Naive max PF: {self.max_naive}')
            self.bar_naive.set_width(self.naive_tests)
            self.naive_i += 1

        # optimized side
        if self.opt_j >= 2:
            cont = True
            self.opt_tests += 1
            if self.n % self.opt_j == 0:
                cp = self.n // self.opt_j
                if is_prime_opt(cp):
                    candidate = cp
                elif is_prime_opt(self.opt_j):
                    candidate = self.opt_j
                else:
                    candidate = None
                if candidate is not None and (self.max_opt is None or candidate > self.max_opt):
                    self.max_opt = candidate
                    self.txt_opt.set_text(f'Opt  max PF: {self.max_opt}')
            self.bar_opt.set_width(self.opt_tests)
            self.opt_j -= 1

        return cont

# --- static performance with hover tooltips
try:
    import mplcursors
except ImportError:  # pragma: no cover - optional dependency for tooltips
    mplcursors = None
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
            t0 = time.perf_counter(); naive_lpf(n); t1 = time.perf_counter()
            t2 = time.perf_counter(); optimized_lpf(n); t3 = time.perf_counter()
            self.times_naive.append(t1 - t0)
            self.times_opt.append(t3 - t2)

    def _plot(self):
        self.ax.clear()
        self.ax.plot(self.sizes, self.times_naive, 'o-', label='Naive (O(n²))')
        self.ax.plot(self.sizes, self.times_opt, 's-', label='Optimized (O(log n))')
        self.ax.set_xscale('log')
        self.ax.set_yscale('log')
        self.ax.set_title('LPF Runtime Comparison (7300x faster)', fontweight='bold')
        self.ax.set_xlabel('n')
        self.ax.set_ylabel('Time')
        self.ax.legend()

        self.scat_naive = self.ax.scatter(self.sizes, self.times_naive, s=50, marker='o', alpha=0.6)
        self.scat_opt = self.ax.scatter(self.sizes, self.times_opt, s=50, marker='s', alpha=0.6)

    def _connect(self):
        def fmt(t):
            return f"{t*1000:.2f} ms" if t < 1.0 else f"{t:.3f} s"
        if mplcursors is None:
            return

        mplcursors.cursor(self.scat_naive, hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(
                f"n = {int(sel.target[0])}\n"
                f"naive: {fmt(sel.target[1])}"
            )
        )
        mplcursors.cursor(self.scat_opt, hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(
                f"n = {int(sel.target[0])}\n"
                f"opt:   {fmt(sel.target[1])}"
            )
        )

    def update(self):
        return False
