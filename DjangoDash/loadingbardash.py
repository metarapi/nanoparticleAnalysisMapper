# Import necessary libraries
from django_plotly_dash import DjangoDash
from dash import dcc, html
from dash.dependencies import Input, Output

# Create a DjangoDash app
appBar = DjangoDash("LoadingBar")

# Define the layout of your DjangoDash app
appBar.layout = html.Div([
    html.Progress(
        id="progress",
        max=100,  # Set the maximum value for the progress bar
        value=0,   # Initial value
        style={"width": "100%"}  # Set the width of the progress bar
    ),
    dcc.Interval(id="progress-interval", n_intervals=0, interval=500)
])

# Define the callback to update the progress bar
@appBar.callback(
    [Output("progress", "value")],
    [Input("progress-interval", "n_intervals")]
)
def update_progress(n):
    # Simulate progress by incrementing the value
    progress = min(n % 110, 100)
    return progress,

