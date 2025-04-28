import numpy as np
import math

class EnhancedCollatz:
    def __init__(self, seeds, fig):
        self.seeds = seeds
        self.fig = fig
        self.paused = False
        self.step = 1

        # build & cache full sequences
        self.cache = {1: [1]}
        self.seqs = [self._get_sequence(s) for s in seeds]

        # compute bounds & histogram bins
        self.max_len = max(len(seq) for seq in self.seqs)
        self.global_max = max(max(seq) for seq in self.seqs)
        self.bins = np.logspace(0, math.log10(self.global_max), num=20)

        self._setup()

    def _get_sequence(self, n):
        seq = []
        x = n
        while x not in self.cache:
            seq.append(x)
            x = x // 2 if x % 2 == 0 else 3 * x + 1
        full = seq + self.cache[x]
        self.cache[n] = full
        return full

    def _setup(self):
        # clear & create two stacked axes
        self.fig.clear()
        self.ax_main, self.ax_hist = self.fig.subplots(
            2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 1]}
        )

        # —— Main plot (log‐scale)
        self.ax_main.set_title(f'Enhanced Collatz – seeds {self.seeds}', fontweight='bold')
        self.ax_main.set_ylabel('Value (log scale)')
        self.ax_main.set_yscale('log')
        self.ax_main.set_xlim(0, self.max_len)
        self.ax_main.set_ylim(1, self.global_max * 1.1)

        # one line + scatter per seed
        colors = ['tab:blue', 'tab:green', 'tab:purple', 'tab:brown']
        self.lines, self.scatters = [], []
        for idx, seed in enumerate(self.seeds):
            col = colors[idx % len(colors)]
            line, = self.ax_main.plot([], [], '-', color=col, label=f'seed {seed}')
            sc = self.ax_main.scatter([], [], s=50, edgecolors='black')
            self.lines.append(line)
            self.scatters.append(sc)
        self.ax_main.legend(loc='upper right')

        # annotation for seed 0’s current value
        self.annot = self.ax_main.text(
            0, self.seqs[0][0], str(self.seqs[0][0]),
            fontsize=10, ha='left', va='bottom'
        )

        # peak‐value line for seed 0
        self.peak = self.seqs[0][0]
        self.peak_line = self.ax_main.axhline(
            self.peak, color='orange', linestyle='--', label='seed 0 peak'
        )

        # —— Histogram subplot (set scale & grid, no initial hist)
        self.ax_hist.set_xscale('log')
        self.ax_hist.set_yscale('log')
        self.ax_hist.set_xlabel('Value')
        self.ax_hist.set_ylabel('Count')
        self.ax_hist.grid(True, which='both', ls='--', lw=0.5)

        self.fig.tight_layout()

    def toggle_pause(self):
        self.paused = not self.paused

    def update(self):
        if self.paused:
            return True

        if self.step > self.max_len:
            return False

        xs = list(range(self.step))
        all_vals = []

        for idx, seq in enumerate(self.seqs):
            ys = seq[:self.step] if self.step <= len(seq) else seq
            all_vals.extend(ys)

            # update line
            self.lines[idx].set_data(xs, ys)

            # update parity‐colored scatter
            offsets = np.column_stack((xs, ys))
            colors = ['blue' if y % 2 == 0 else 'red' for y in ys]
            self.scatters[idx].set_offsets(offsets)
            self.scatters[idx].set_facecolors(colors)

        # annotate seed 0’s current value
        y0 = self.seqs[0][self.step - 1] if self.step - 1 < len(self.seqs[0]) else self.seqs[0][-1]
        self.annot.set_position((self.step - 1, y0))
        self.annot.set_text(str(y0))

        # update peak line if needed
        if y0 > self.peak:
            self.peak = y0
            self.peak_line.set_ydata([self.peak, self.peak])

        # redraw histogram
        self.ax_hist.cla()
        self.ax_hist.set_xscale('log')
        self.ax_hist.set_yscale('log')
        self.ax_hist.set_xlabel('Value')
        self.ax_hist.set_ylabel('Count')
        self.ax_hist.grid(True, which='both', ls='--', lw=0.5)
        self.ax_hist.hist(all_vals, bins=self.bins, log=True)

        self.fig.tight_layout()
        self.step += 1
        return True
