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

# import numpy as np
# import matplotlib.pyplot as plt
# from data_processing import process_file

# # Create a numpy array with 1000 rows and 2 columns
# # The first column will go from 0 to 1000
# # Second column will be all ones
# array = np.ones((1000,2))
# array[:,0] = np.linspace(0,1000,1000)
# # Pick a few random numbers in the second column and add a random number from 10 to 100 to them
# array[np.random.randint(0,1000,10),1] += np.random.randint(10,100,10)
# # Define a simple 1D kernel
# kernel = np.array([0.05,0.15,0.4,0.3,0.1])
# # Convolve the second column of the array with the kernel
# array[:,1] = np.convolve(array[:,1],kernel,mode='same')

# # Save this array as a .csv file. This is the file that will be read in by the process_file function
# np.savetxt('test.csv', array, delimiter=',')

# # Get the path to the file
# file_path = 'test.csv'

# # Call the process_file function
# detections, labels, regions = process_file(file_path, convertToCounts=False)

# # Display the results
# print("Detections:", detections)
# print("Regions:", regions)
# print(len(labels))

# # Crop the array. Remove the top 4 rows and the bottom 3 rows
# array = array[4:-3,:]

# plt.plot(array[:, 0], array[:, 1])
# plt.plot(array[regions[:, 0], 0], array[regions[:, 0], 1], 'ro')
# plt.plot(array[regions[:, 1], 0], array[regions[:, 1], 1], 'go')

# plt.show()

## Generate data

import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import scipy.signal as signal

def gaussian_kernel(n, std, normalised=False):
    '''
    Generates a n x n matrix with a centered gaussian 
    of standard deviation std centered on it. If normalised,
    its volume equals 1.'''
    gaussian1D = signal.gaussian(n, std)
    gaussian2D = np.outer(gaussian1D, gaussian1D)
    if normalised:
        gaussian2D /= (2*np.pi*(std**2))
    return gaussian2D

arraySize = 500
startPoint = -250

x = np.linspace(startPoint, arraySize-startPoint ,arraySize)
y = x

radius = 125

array = np.zeros((arraySize,arraySize))

for i in x:
    for j in y:
        idxX = int(i-1)+250
        idxY = int(j-1)+250
        if (np.sqrt(i**2+j**2) < radius*1.01) and (np.sqrt(i**2+j**2) > radius*0.99):
        #if round(np.sqrt(i**2+j**2)) == radius:
            array[idxX,idxY] = 1

# Gaussian 2D gaussian kernel with size of 5x5
kernel = gaussian_kernel(5,1.5,normalised=True)

# kernel = np.array([[1,1,1,1,1],
#                    [1,1,2,2,1],
#                    [1,2,3,2,1],
#                    [1,2,2,2,1],
#                    [1,1,1,1,1]])

probabiltyMap = signal.convolve2d(array,kernel)
probabiltyMap = probabiltyMap/np.max(probabiltyMap)

np.savetxt('probabilityMap.csv', probabiltyMap, delimiter=',')

plt.imshow(array)
plt.imshow(probabiltyMap)
plt.show()
