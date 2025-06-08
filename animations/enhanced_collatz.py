import numpy as np
import math

class EnhancedCollatz:
    def __init__(self, seeds, fig):
        # Validate seeds: only accept positive integers.
        if any(s <= 0 for s in seeds):
            raise ValueError("All seeds must be positive integers.")
        self.seeds = seeds
        self.fig = fig
        self.paused = False
        self.step = 1

        # Build & cache the full Collatz sequences
        self.cache = {1: [1]}
        self.seqs = [self._get_sequence(s) for s in seeds]

        # For plotting bounds & histogram bins
        self.max_len    = max(len(seq) for seq in self.seqs)
        self.global_max = max(max(seq) for seq in self.seqs)
        self.bins       = np.logspace(0, math.log10(self.global_max), num=20)

        self._setup()

    def _get_sequence(self, n):
        # Extra validation in case a non-positive number slips through
        if n <= 0:
            raise ValueError("Seed must be a positive integer.")
        seq = []
        x = n
        while x not in self.cache:
            seq.append(x)
            x = x // 2 if x % 2 == 0 else 3 * x + 1
        full = seq + self.cache[x]
        self.cache[n] = full
        return full

    def _setup(self):
        self.fig.clear()
        self.ax_main, self.ax_hist = self.fig.subplots(
            2, 1, sharex=True, gridspec_kw={'height_ratios': [3,1]}
        )

        # Main panel: log‐scale line + parity scatter
        self.ax_main.set_title(f'Enhanced Collatz – seeds {self.seeds}', fontweight='bold')
        self.ax_main.set_ylabel('Value (log scale)')
        self.ax_main.set_yscale('log')
        self.ax_main.set_xlim(0, self.max_len)
        self.ax_main.set_ylim(1, self.global_max * 1.1)

        colors = ['tab:blue','tab:green','tab:purple','tab:brown']
        self.lines = []
        self.scatters = []
        for idx, seed in enumerate(self.seeds):
            col = colors[idx % len(colors)]
            line, = self.ax_main.plot([], [], '-', color=col, label=f'seed {seed}')
            sc = self.ax_main.scatter([], [], s=50, edgecolors='black', color=col)
            self.lines.append(line)
            self.scatters.append(sc)
        self.ax_main.legend(loc='upper right')

        # Annotation & peak‐line for the FIRST seed
        init0 = self.seqs[0][0]
        self.annot = self.ax_main.text(0, init0, str(init0),
                                       fontsize=10, ha='left', va='bottom')
        self.peak = init0
        self.peak_line = self.ax_main.axhline(self.peak,
                                              color='orange',
                                              linestyle='--')

        # Histogram panel: grid only (no log‐scale yet)
        self.ax_hist.set_xlabel('Value')
        self.ax_hist.set_ylabel('Count')
        self.ax_hist.grid(True, which='both', ls='--', lw=0.5)

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

            # update parity scatter
            # handle sequences shorter than the current step
            pts = np.column_stack((xs[:len(ys)], ys))
            fc  = ['blue' if y % 2 == 0 else 'red' for y in ys]
            self.scatters[idx].set_offsets(pts)
            self.scatters[idx].set_facecolors(fc)

        # update annotation & peak for seed0
        y0 = self.seqs[0][self.step-1] if self.step-1 < len(self.seqs[0]) else self.seqs[0][-1]
        self.annot.set_position((self.step-1, y0))
        self.annot.set_text(str(y0))
        if y0 > self.peak:
            self.peak = y0
            self.peak_line.set_ydata([self.peak, self.peak])

        # build a simple histogram of all seen values
        counts, edges = np.histogram(all_vals, bins=self.bins)

        # clear & label
        self.ax_hist.clear()
        self.ax_hist.set_xlabel('Value')
        self.ax_hist.set_ylabel('Count')
        self.ax_hist.grid(True, which='both', ls='--', lw=0.5)

        # only draw & log-scale if there's at least one nonzero bin
        mask = counts > 0
        if mask.any():
            centers = (edges[:-1] + edges[1:]) * 0.5
            widths  = edges[1:] - edges[:-1]
            self.ax_hist.bar(centers[mask], counts[mask],
                            width=widths[mask], align='center')
            # now it's safe to switch to log scales
            try:
                self.ax_hist.set_xscale('log')
                self.ax_hist.set_yscale('log')
            except ValueError:
                # if something still balks, fall back to linear
                self.ax_hist.set_xscale('linear')
                self.ax_hist.set_yscale('linear')
        else:
            # no data yet → keep both axes linear
            self.ax_hist.set_xscale('linear')
            self.ax_hist.set_yscale('linear')

        self.fig.tight_layout()
        self.step += 1
        return True
