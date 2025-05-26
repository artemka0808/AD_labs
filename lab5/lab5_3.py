import dash
from dash import dcc, html, Input, Output, ctx
import numpy as np
import plotly.graph_objs as go

time = np.linspace(0, 1, 500)
noise_data = np.zeros_like(time)
noise_generated = False

# EMA фільтр
def exponential_moving_average(signal, alpha):
    filtered = np.zeros_like(signal)
    filtered[0] = signal[0]
    for i in range(1, len(signal)):
        filtered[i] = alpha * signal[i] + (1 - alpha) * filtered[i - 1]
    return filtered

def createSlider(id, min_val, max_val, step, val, label):
    return html.Div([
        html.Label(label),
        dcc.Slider(id=id, min=min_val, max=max_val, step=step, value=val,
                   marks={min_val: str(min_val), max_val: str(max_val)},
                   tooltip={"placement": "top", "always_visible": True})
    ])

# Dash app
app = dash.Dash(__name__)
app.title = "EMA Filter App"

# Layout
app.layout = html.Div([
    html.H2("Signal with Exponential Moving Average (EMA) Filter"),

    dcc.Graph(id='graph'),

    html.Div([
        createSlider('Amplitude', 0.1, 5, 0.01, 0.97, 'Amplitude'),
        createSlider('Frequency', 0.1, 10, 0.01, 0.27, 'Frequency'),
        createSlider('Phase', 0, 2 * np.pi, 0.01, 0, 'Phase'),
        createSlider('Noise Mean', -2, 2, 0.01, 0.4, 'Noise Mean'),
        createSlider('Noise Covariance', 0, 1, 0.01, 0.4, 'Noise Covariance'),
        createSlider('Alpha EMA', 0.01, 1.0, 0.01, 0.2, 'Alpha EMA'),

        html.Label("Display Mode:"),
        dcc.Dropdown(
            id='mode',
            options=[
                {'label': 'Signal', 'value': 'signal'},
                {'label': 'Signal + Noise', 'value': 'signal_noise'},
                {'label': 'Signal + Filter', 'value': 'signal_filter'},
                {'label': 'All', 'value': 'all'},
            ],
            value='all',
            clearable=False,
            style={'width': '220px'}
        ),

        html.Label("Theme:"),
        dcc.Dropdown(
            id='theme',
            options=[
                {'label': 'Light', 'value': 'light'},
                {'label': 'Dark', 'value': 'dark'},
                {'label': 'Colorful', 'value': 'colorful'},
            ],
            value='light',
            clearable=False,
            style={'width': '220px'}
        ),

        html.Br(),
        html.Button("Reset", id="reset", n_clicks=0)
    ], style={'width': '90%', 'margin': 'auto', 'padding': '10px'})
])

@app.callback(
    Output('Amplitude', 'value'),
    Output('Frequency', 'value'),
    Output('Phase', 'value'),
    Output('Noise Mean', 'value'),
    Output('Noise Covariance', 'value'),
    Output('Alpha EMA', 'value'),
    Input('reset', 'n_clicks'),
    prevent_initial_call=True
)
def reset_all(n):
    return 0.97, 0.27, 0, 0.4, 0.4, 0.2

# Update graph
@app.callback(
    Output('graph', 'figure'),
    Input('Amplitude', 'value'),
    Input('Frequency', 'value'),
    Input('Phase', 'value'),
    Input('Noise Mean', 'value'),
    Input('Noise Covariance', 'value'),
    Input('Alpha EMA', 'value'),
    Input('mode', 'value'),
    Input('theme', 'value'),
)
def update_graph(amplitude, frequency, phase, noise_mean, noise_covariance, alpha, mode, theme):
    global noise_data, noise_generated

    y = amplitude * np.sin(2 * np.pi * frequency * time + phase)

    if not noise_generated or ctx.triggered_id in ['Noise Mean', 'Noise Covariance', 'reset']:
        noise_data = np.random.normal(noise_mean, noise_covariance, size=time.shape)
        noise_generated = True

    y_noise = y + noise_data
    y_filtered = exponential_moving_average(y_noise, alpha)

    if theme == 'light':
        bg_color = 'white'
        grid_color = 'lightgray'
        line_colors = ['blue', 'orange', 'green']
        font_color = 'black'
    elif theme == 'dark':
        bg_color = '#1e1e1e'
        grid_color = 'gray'
        line_colors = ['cyan', 'magenta', 'lime']
        font_color = 'white'
    else:  # colorful
        bg_color = '#fffbe6'
        grid_color = '#ddd'
        line_colors = ['#e6194B', '#3cb44b', '#ffe119']
        font_color = 'black'

    fig = go.Figure()

    if mode in ['signal', 'signal_noise', 'signal_filter', 'all']:
        fig.add_trace(go.Scatter(x=time, y=y, mode='lines', name='Signal', line=dict(color=line_colors[0])))

    if mode in ['signal_noise', 'all']:
        fig.add_trace(go.Scatter(x=time, y=y_noise, mode='lines', name='Noise', line=dict(color=line_colors[1])))

    if mode in ['signal_filter', 'all']:
        fig.add_trace(go.Scatter(x=time, y=y_filtered, mode='lines', name='Filtered (EMA)', line=dict(color=line_colors[2])))

    fig.update_layout(
        height=500,
        margin=dict(l=30, r=20, t=30, b=30),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font_color=font_color,
        xaxis=dict(showgrid=True, gridcolor=grid_color),
        yaxis=dict(showgrid=True, gridcolor=grid_color)
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
