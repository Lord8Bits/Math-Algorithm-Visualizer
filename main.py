import matplotlib
matplotlib.use('TkAgg')      # before pyplot
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from animations.collatz import EnhancedCollatz
from animations.prime_factor import (
    DualPrimeFactorProgression,
    PrimeFactorPerformance
)

# —— GUI layout
layout = [
    [sg.Text('Project Euler Visualizer', font=('Arial', 16))],
    [
        sg.Button('Enhanced Collatz'),
        sg.Button('LPF Dual Progression'),
        sg.Button('LPF Performance'),
        sg.Button('Exit')
    ],
    [
        sg.Button('Pause/Play', key='-PAUSE-'),
        sg.Text('Speed (ms):'),
        sg.Slider(range=(10, 1000), default_value=200, orientation='h',
                  size=(20, 15), key='-SPEED-')
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
    # update speed from slider
    speed = int(values.get('-SPEED-', speed))

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    # pause/play toggle
    if event == '-PAUSE-':
        if animator and hasattr(animator, 'toggle_pause'):
            animator.toggle_pause()
        continue

    # Enhanced Collatz
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
        canvas.draw()
        window.refresh()
        continue

    # LPF Dual Progression
    if event == 'LPF Dual Progression':
        inp = sg.popup_get_text(
            'Enter n for LPF dual progression (e.g. 13195)',
            'LPF Dual Progression',
            default_text='13195'
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
        canvas.draw()
        window.refresh()
        continue

    # LPF Performance
    if event == 'LPF Performance':
        fig.clear()
        ax = fig.add_subplot(111)
        sizes = [
            10_000, 20_000, 50_000,
            100_000, 200_000, 500_000,
            1_000_000, 2_000_000
        ]
        animator = PrimeFactorPerformance(sizes, ax)
        canvas.draw()
        window.refresh()
        continue

    # run one animation step
    if animator:
        try:
            cont = animator.update()
            if cont:
                canvas.draw()
                window.refresh()
            else:
                animator = None
        except Exception as e:
            print('Animation Error:', e)
            animator = None

window.close()
