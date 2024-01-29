# # Q: Create a plotly scatter plot of the of a sine wave where I can change the frequency and amplitude of the wave using sliders.

# import plotly.graph_objects as go

# import numpy as np

# from scipy import signal

# import dash

# import dash_core_components as dcc

# import dash_html_components as html

# from dash.dependencies import Input, Output

# app = dash.Dash()

# app.layout = html.Div([
#     dcc.Graph(id="graph"),
#     html.Label([
#         "Frequency",
#         dcc.Slider(
#             id="freq-slider",
#             min=1,
#             max=10,
#             step=0.5,
#             value=1,
#             marks={i: str(i) for i in range(10)},
#         ),
#     ]),

#     html.Label([
#         "Amplitude",
#         dcc.Slider(
#             id="amp-slider",
#             min=1,
#             max=10,
#             step=0.5,
#             value=1,
#             marks={i: str(i) for i in range(10)},
#         ),
#     ]),
# ])

# @app.callback(
#     Output("graph", "figure"),
#     [Input("freq-slider", "value"),
#      Input("amp-slider", "value")])
# def display_sine(freq, amp):
#     x = np.linspace(0, 10, 1000)
#     y = amp * np.sin(freq * x)
#     fig = go.Figure(data=go.Scatter(x=x, y=y, mode="lines"))
#     return fig


# if __name__ == "__main__":
#     app.run_server(debug=True)



# import numpy as np
# from lib import spcalext

# # Create a sample dataset
# x = np.array([1.0, 2.0, 3.0, 2.0, 1.0, 4.0, 5.0, 4.0, 3.0, 2.0])

# # Define the regions of interest
# regions = np.array([[0, 5], [5, 10]])

# # Call the maxima function from the spcalext module
# maxima = spcalext.maxima(x, regions)

# # Print the results
# print("Input array:", x)
# print("Regions:", regions)
# print("Maxima:", maxima)

# Here we're going to test the data_processing.py file funcions and their output

import numpy as np
import matplotlib.pyplot as plt
from data_processing import process_file
from scipy import signal
import poisson, detection

# Define the path to the file
file_path = "D:/DjangoCoding/NPAnalysisMapper/mysite/generated/linescan_100.csv"

# Read the file into a numpy array
array = np.genfromtxt(file_path, delimiter=',', skip_header=4, skip_footer=3)
filtered_array = signal.medfilt(array[:, 1], 25)

if np.mean(filtered_array) < 10:
    epsilon = 0.5
else:
    epsilon = 0

Sc, Sd = poisson.currie(filtered_array, epsilon=epsilon)

# detections, labels, regions = detection.accumulate_detections(array[:,1], Sc, Sd, integrate=True)

# Call the process_file function
detections, labels, regions = process_file(file_path, convertToCounts=False)

# Crop the array. Remove the top 4 rows and the bottom 3 rows
# array = array[4:-3,:]

plt.plot(array[:, 0], array[:, 1])
plt.plot(filtered_array, 'b--')
plt.plot(Sc, 'r--')
plt.plot(Sd, 'g--')
plt.plot(array[regions[:, 0], 0], array[regions[:, 0], 1], 'ro')
plt.plot(array[regions[:, 1], 0], array[regions[:, 1], 1], 'go')
plt.legend(['Raw Data', 'Filtered Data', 'Sc', 'Sd', 'Start', 'End'])

plt.show()

#print("Detections:", detections)
#print("Regions:", regions)

print('Mean:', np.mean(filtered_array))
print('Sc:', Sc)
print('Sd:', Sd)
