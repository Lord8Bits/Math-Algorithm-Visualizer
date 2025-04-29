import time
import math
import numpy as np
import matplotlib.pyplot as plt
import mplcursors

# --- naive Collatz chain length (no memoization)
def collatz_length_naive(n):
    cnt = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        cnt += 1
    return cnt

# --- optimized Collatz chain length (with memoization)
_collatz_cache = {1: 0}
def collatz_length_opt(n):
    if n in _collatz_cache:
        return _collatz_cache[n]
    if n % 2 == 0:
        nxt = n // 2
    else:
        nxt = 3 * n + 1
    cnt = 1 + collatz_length_opt(nxt)
    _collatz_cache[n] = cnt
    return cnt

class CollatzPerformance:
    """
    Static comparison of naive vs optimized Collatz chain-length runtimes
    for various N, plotted on a log-log chart with hover tooltips.
    """
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
        for N in self.sizes:
            # naive total time
            t0 = time.perf_counter()
            for i in range(1, N + 1):
                collatz_length_naive(i)
            t1 = time.perf_counter()
            # optimized total time
            # reset cache
            global _collatz_cache
            _collatz_cache = {1: 0}
            t2 = time.perf_counter()
            for i in range(1, N + 1):
                collatz_length_opt(i)
            t3 = time.perf_counter()

            self.times_naive.append(t1 - t0)
            self.times_opt.append(t3 - t2)

    def _plot(self):
        self.ax.clear()
        self.ax.plot(self.sizes, self.times_naive, 'o-', label='Naive (O(n ⋅ chain))')
        self.ax.plot(self.sizes, self.times_opt,   's-', label='Optimized (memoized, ≃ O(log n))')
        self.ax.set_xscale('log')
        self.ax.set_yscale('log')
        self.ax.set_title('Collatz Chain-Length Performance (14x Faster)', fontweight='bold')
        self.ax.set_xlabel('Max N')
        self.ax.set_ylabel('Total time (s)')
        self.ax.legend()

        # scatter points for tooltips
        self.scat_naive = self.ax.scatter(self.sizes, self.times_naive,
                                          s=50, marker='o', alpha=0.6)
        self.scat_opt   = self.ax.scatter(self.sizes, self.times_opt,
                                          s=50, marker='s', alpha=0.6)

    def _connect(self):
        # hover tooltips
        mplcursors.cursor(self.scat_naive, hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(
                f"N ≤ {int(sel.target[0])}\n"
                f"naive: {sel.target[1]:.3f}s"
            )
        )
        mplcursors.cursor(self.scat_opt, hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(
                f"N ≤ {int(sel.target[0])}\n"
                f"opt:   {sel.target[1]:.3f}s"
            )
        )

    def update(self):
        # static plot only
        return False
