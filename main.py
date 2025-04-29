import matplotlib
matplotlib.use('TkAgg')
import PySimpleGUI as sg
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from animations.collatz_performance import CollatzPerformance
from animations.enhanced_collatz import EnhancedCollatz
from animations.prime_factor import (
    DualPrimeFactorProgression,
    PrimeFactorPerformance
)

# —— GUI layout
layout = [
    [sg.Text('Project Euler Visualizer', font=('Arial', 16))],
    [
        sg.Button('Enhanced Collatz'),
        sg.Button('Collatz Performance'),
        sg.Button('LPF Dual Progression'),
        sg.Button('LPF Performance'),

        sg.Button('Exit')
    ],
    [
        sg.Button('Pause/Play', key='-PAUSE-'),
        sg.Text('Speed (ms):'),
        sg.Slider(range=(10, 1000),
                  default_value=200,
                  orientation='h',
                  size=(20, 15),
                  key='-SPEED-')
    ],
    [sg.Canvas(key='-CANVAS-', size=(800, 500))]
]

window = sg.Window('Euler Visualizer', layout, finalize=True)

fig = plt.figure(figsize=(8, 5))
canvas = FigureCanvasTkAgg(fig, master=window['-CANVAS-'].TKCanvas)
canvas.draw()
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

animator = None
speed = 200

while True:
    event, values = window.read(timeout=speed)
    speed = int(values.get('-SPEED-', speed))

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == '-PAUSE-':
        if animator and hasattr(animator, 'toggle_pause'):
            animator.toggle_pause()
        continue

    if event == 'Enhanced Collatz':
        inp = sg.popup_get_text(
            'Enter seed(s), comma-separated (e.g. 27,13)',
            'Enhanced Collatz',
            default_text='27,13'
        )
        if not inp:
            continue
        try:
            seeds = [int(s.strip()) for s in inp.split(',')]
        except ValueError:
            sg.popup_error('Please enter integers separated by commas.')
            continue
        animator = EnhancedCollatz(seeds, fig)
        canvas.draw(); window.refresh()
        continue
    if event == 'Collatz Performance':
       fig.clear()
       ax = fig.add_subplot(111)
       # e.g. test up to 10k,20k,40k,80k for speed
       sizes = [10_000 * 2**i for i in range(7)]
       animator = CollatzPerformance(sizes, ax)
       canvas.draw(); window.refresh()
       continue

    if event == 'LPF Dual Progression':
        inp = sg.popup_get_text(
            'Enter n for LPF dual progression (e.g. 180)',
            'LPF Dual Progression',
            default_text='180'
        )
        if not inp:
            continue
        try:
            n = int(inp)
        except ValueError:
            sg.popup_error('Please enter a valid integer.')
            continue
        fig.clear()
        ax = fig.add_subplot(111)
        animator = DualPrimeFactorProgression(n, ax)
        canvas.draw(); window.refresh()
        continue

    if event == 'LPF Performance':
        fig.clear()
        ax = fig.add_subplot(111)
        # a richer, geometric progression from 10 000 up to ~2.56 million
        sizes = [10_000 * (2**i) for i in range(0, 15)]  # [10k, 20k, 40k, …, 2 560k]
        # insert one mid-range check for extra detail
        sizes.insert(2, 30_000)  # now: 10k, 20k, 30k, 40k, …, 2 560k
        animator = PrimeFactorPerformance(sizes, ax)
        canvas.draw(); window.refresh()
        continue

    # animation stepping
    if animator:
        try:
            cont = animator.update()
            if cont:
                canvas.draw(); window.refresh()
            else:
                animator = None
        except Exception as e:
            print('Animation Error:', e)
            animator = None

window.close()
