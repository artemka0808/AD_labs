import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Slider, RangeSlider, Button, CheckButtons
import numpy as np
from scipy.signal import butter, filtfilt

def sidebar(fig, sidebar_grid, redraw):
    sliders = {}

    showNoise_ax = fig.add_axes([0.1, 0.03, 0.15, 0.03])
    showNoise = CheckButtons(showNoise_ax, ['Show Noise'], [True])
    showNoise.on_clicked(lambda label: redraw(False))

    showFilter_ax = fig.add_axes([0.3, 0.03, 0.15, 0.03])
    showFilter = CheckButtons(showFilter_ax, ['Show Filter'], [True])
    showFilter.on_clicked(lambda label: redraw(False))

    param_names = [
        ('Amplitude', (0.1, 5, 0.97)),
        ('Frequency', (0.1, 10, 0.27)),
        ('Phase', (0, 2 * np.pi, 0)),
        ('Noise Mean', (-2, 2, 0.4)),
        ('Noise Covariance', (0, 1, 0.4)),
        ('Cutoff Frequency', (0.01, 50, 5))
    ]

    slider_axes = []
    start_y = 0.35
    for i, (name, (min_val, max_val, def_val)) in enumerate(param_names):
        ax = fig.add_axes([0.1, start_y - i * 0.05, 0.8, 0.03])  # x, y, w, h
        sliders[name] = Slider(ax, name, min_val, max_val, valinit=def_val)
        sliders[name].on_changed(lambda val, name=name: redraw(name in ['Noise Mean', 'Noise Covariance']))

    # R
    reset_ax = fig.add_axes([0.8, 0.02, 0.1, 0.04])
    reset_btn = Button(reset_ax, 'Reset')

    def reset(event):
        for s in sliders.values():
            s.reset()
        redraw(True)

    reset_btn.on_clicked(reset)

    return sliders, showNoise, showFilter

def appWindow():
    fig = plt.figure(figsize=(12, 8))
    main_grid = GridSpec(nrows=2, ncols=1, figure=fig, height_ratios=[3, 3], hspace=0.5)

    ax_plot = fig.add_subplot(main_grid[0])

    signal_line = noise_line = filtered_line = None
    noise_data = None

    def updatePlot(redraw_noise):
        nonlocal signal_line, noise_line, filtered_line, noise_data
        time = np.linspace(0, 10, 1000)
        amplitude = sliders['Amplitude'].val
        frequency = sliders['Frequency'].val
        phase = sliders['Phase'].val

        y = amplitude * np.sin(2 * np.pi * frequency * time + phase)

        if signal_line is None:
            signal_line, = ax_plot.plot(time, y, label='Signal', color='blue')
        else:
            signal_line.set_ydata(y)

        if redraw_noise or noise_data is None:
            mean = sliders['Noise Mean'].val
            cov = sliders['Noise Covariance'].val
            noise_data = np.random.normal(mean, cov, size=time.shape)
        y_noise = y + noise_data

        if showNoise.get_status()[0]:
            if noise_line is None:
                noise_line, = ax_plot.plot(time, y_noise, label='Noisy Signal', color='orange', alpha=0.6)
            else:
                noise_line.set_ydata(y_noise)
        else:
            if noise_line:
                noise_line.remove()
                noise_line = None

        if showFilter.get_status()[0]:
            cutoff = sliders['Cutoff Frequency'].val
            b, a = butter(N=4, Wn=cutoff, btype='low', fs=1000)
            filtered = filtfilt(b, a, y_noise)

            if filtered_line is None:
                filtered_line, = ax_plot.plot(time, filtered, label='Filtered', color='red')
            else:
                filtered_line.set_ydata(filtered)
        else:
            if filtered_line:
                filtered_line.remove()
                filtered_line = None

        ax_plot.relim()
        ax_plot.autoscale_view()
        ax_plot.legend()
        fig.canvas.draw_idle()

    sliders, showNoise, showFilter = sidebar(fig, main_grid[1], updatePlot)

    updatePlot(True)
    plt.show()

if __name__ == '__main__':
    appWindow()