# Algorithm Visualizer & Benchmark Suite

![Python](https://img.shields.io/badge/language-Python-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/build-passing-brightgreen)

> **Original Concept:** A _volatile_ framework that runs multiple implementations of the same algorithm side-by-side, measures their runtime performance, and ranks them dynamically.

---

## Project Overview

This toolkit provides:

1. **Interactive Animations** of classic algorithms:
   - **Enhanced Collatz**: Visualize Collatz sequences with parity scatter and histogram. (work in progress)
   - **LPF Dual Progression**: Step-by-step comparison of naive vs. optimized largest-prime-factor methods.

2. **Static Benchmark Plots**:
   - **LPF Performance**: Log–log chart of naive vs. optimized LPF runtimes, with hoverable tooltips. 
   - **Collatz Performance**: Compare naive chain-length vs. memoized (optimized) runtimes for Collatz across ranges.

3. **Automated Ranking**:
   - Each routine records timings, converts to ms/s, and can be extended to output relative speed-up factors.

4. **Extensible Design**:
   - Drop-in modules under `animations/` can be swapped or extended with new algorithms.  
   - Central `main.py` GUI (PySimpleGUI + Matplotlib).

---

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/algorithm-visualizer.git
   cd algorithm-visualizer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the GUI**
   ```bash
   python main.py
   ```


---

## Usage

1. **Launch** the application.
2. **Select** one of the buttons:
   - **LPF Dual Progression**: Enter an integer _n_ to see divisor test progress bars.  
   - **LPF Performance**: Auto-generates a log–log runtime comparison of naive vs. optimized LPF for a geometric series of _n_.  
   - **Collatz Performance**: Benchmarks naive vs. memoized chain-length over increasing _N_.  
3. **Hover** over plotted points to reveal precise timings (auto-scaled to ms or s).
4. **Pause/Play** animations with the `Pause/Play` button.

---

## Features & Highlights

- **Real-time Speed-Up Display**: Easily see how many × faster one approach is over another.  
- **Tooltip Formatting**: Milliseconds for sub-second times, seconds for longer runs.  
- **Volatile Benchmarking**: Designed to let you plug in **any** pair of algorithms for quick runtime ranking. (not yet implemented)
- **Modern Look & Feel**: Uses Matplotlib styles (`ggplot` by default) for polished charts.

---

## Contributing

 **Suggestions for enhancements are welcome:**

- Add new algorithms under `animations/` and register buttons in `main.py`.  
- Improve caching or introduce probabilistic tests (e.g., Miller–Rabin) for prime checks. (and please explain it me if you could 😭)
- Enhance UI (themes, more interactivity) or export options (CSV, PDF). (program is very bland any improvement to UI is accepted)

---

## License

This project is released under the **MIT License**. See [LICENSE](LICENSE) for details.


