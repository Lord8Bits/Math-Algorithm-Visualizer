import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("ggplot")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from animations.collatz_performance import CollatzPerformance
from animations.enhanced_collatz import EnhancedCollatz
from animations.prime_factor import (
    DualPrimeFactorProgression,
    PrimeFactorPerformance,
)


class App:
    """Tkinter-based GUI for visualizing and benchmarking algorithms."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Euler Visualizer")

        self.speed = tk.IntVar(value=200)
        self.animator = None

        ttk.Label(root, text="Project Euler Visualizer", font=("Arial", 16)).pack(
            pady=5
        )

        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=2)

        ttk.Button(btn_frame, text="Enhanced Collatz", command=self.run_enhanced).grid(
            row=0, column=0, padx=2
        )
        ttk.Button(
            btn_frame, text="Collatz Performance", command=self.run_collatz_perf
        ).grid(row=0, column=1, padx=2)
        ttk.Button(btn_frame, text="LPF Dual Progression", command=self.run_lpf_dual).grid(
            row=0, column=2, padx=2
        )
        ttk.Button(btn_frame, text="LPF Performance", command=self.run_lpf_perf).grid(
            row=0, column=3, padx=2
        )
        ttk.Button(btn_frame, text="Exit", command=root.destroy).grid(
            row=0, column=4, padx=2
        )

        control = ttk.Frame(root)
        control.pack(pady=2)
        ttk.Button(control, text="Pause/Play", command=self.toggle_pause).grid(
            row=0, column=0, padx=2
        )
        ttk.Label(control, text="Speed (ms):").grid(row=0, column=1, padx=2)
        ttk.Scale(control, from_=10, to=1000, orient="horizontal", variable=self.speed).grid(
            row=0, column=2, padx=2
        )

        self.fig = plt.figure(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=1)

        self.root.after(self.speed.get(), self.on_timer)

    # ------------------------------------------------------------------ helpers
    def on_timer(self) -> None:
        """Periodic update callback for animations."""
        if self.animator:
            try:
                cont = self.animator.update()
                if cont:
                    self.canvas.draw()
                else:
                    self.animator = None
            except Exception as exc:  # pragma: no cover - runtime safety
                print("Animation Error:", exc)
                self.animator = None
        self.root.after(self.speed.get(), self.on_timer)

    def toggle_pause(self) -> None:
        if self.animator and hasattr(self.animator, "toggle_pause"):
            self.animator.toggle_pause()

    # -------------------------------------------------------------- button hooks
    def run_enhanced(self) -> None:
        inp = simpledialog.askstring(
            "Enhanced Collatz",
            "Enter seed(s), comma-separated (e.g. 27,13)",
            initialvalue="27,13",
            parent=self.root,
        )
        if not inp:
            return
        try:
            seeds = [int(s.strip()) for s in inp.split(",")]
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter integers separated by commas.", parent=self.root
            )
            return
        self.animator = EnhancedCollatz(seeds, self.fig)
        self.canvas.draw()

    def run_collatz_perf(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        sizes = [10_000 * 2 ** i for i in range(7)]
        self.animator = CollatzPerformance(sizes, ax)
        self.canvas.draw()

    def run_lpf_dual(self) -> None:
        inp = simpledialog.askstring(
            "LPF Dual Progression",
            "Enter n for LPF dual progression (e.g. 180)",
            initialvalue="180",
            parent=self.root,
        )
        if not inp:
            return
        try:
            n = int(inp)
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid integer.", parent=self.root
            )
            return
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        self.animator = DualPrimeFactorProgression(n, ax)
        self.canvas.draw()

    def run_lpf_perf(self) -> None:
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        sizes = [10_000 * (2 ** i) for i in range(15)]
        sizes.insert(2, 30_000)
        self.animator = PrimeFactorPerformance(sizes, ax)
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()

