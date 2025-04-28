import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import animations.euler1

layout = [
    [sg.Text('Project Euler Visualizer')],
    [sg.Button('Problem 1: Sieve'), sg.Button('Exit')],
    [sg.Canvas(key='-CANVAS-', size=(800, 400))]
]

window = sg.Window('Euler Visualizer', layout, finalize=True)

fig, ax = plt.subplots(figsize=(10, 4))
canvas = FigureCanvasTkAgg(fig, window['-CANVAS-'].TKCanvas)
canvas.draw()

animator = None

while True:
    event, values = window.read(timeout=50)  # Faster refresh rate
    
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
        
    if event == 'Problem 1: Sieve':
        animator = animations.euler1.SieveAnimation(30, ax)
        
    if animator:
        if animator.update():
            canvas.draw()
            canvas.flush_events()
        else:
            animator = None

window.close()