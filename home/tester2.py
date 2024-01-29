
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
#from data_processing import process_file
from scipy import signal
import poisson, detection

# Define the path to the file
file_path = "D:/DjangoCoding/NPAnalysisMapper/mysite/generated/linescan_100.csv"

def process_file(
    file_path, 
    convertToCounts=True, 
    medianFilterSize=51, 
    gas_blank_start=0, 
    gas_blank_end=0, 
    number_of_pixels=20):
    
    # Read the file into a pandas dataframe
    df = pd.read_csv(file_path, skiprows=4, skipfooter=3)

    # Convert the dataframe to a numpy array
    array = df.to_numpy()

    # Convert the cps column to counts if necessary
    if convertToCounts:
        array[:,1] = array[:,1] * 0.0001

    # Crop the array based on the gas blank start and end values
    # Each second is 10000 data points (at dwell time of 0.1 ms)
    array = array[gas_blank_start*10000:array.shape[0]-gas_blank_end*10000,:]

    # Filter the data using a median filter with a window size of 51
    filtered_array = signal.medfilt(array[:,1], medianFilterSize)

    # Check if the background is less than 10 counts. If it is, use epsilon of 0.5
    # If the background is greater than 10 counts, use epsilon of 0 
    if np.mean(filtered_array) < 10:
        epsilon = 0.5
    else:
        epsilon = 0

    # Calculate the Sc and Sd values for the data set using the currie function. Use the epsilon value calculated above.
    # Each row in the Sc and Sd arrays corresponds to a row in the data set
    Sc, Sd = poisson.currie(filtered_array, epsilon=epsilon)

    # Use the Sc and Sd values to detect the peaks in the data
    detections, labels, regions = detection.accumulate_detections(array[:,1], Sc, Sd, integrate=True)

    # Obtain the peak areas for each peak
    peak_areas = np.zeros(regions.shape[0])

    for i in range(regions.shape[0]):
        peak_areas[i] = np.sum(array[regions[i,0]:regions[i,1],1])

    # Pad the array with zeros so that it can be reshaped into a 2D array with the specified number of columns
    lineScanSummed = np.pad(array[:,1], (0, number_of_pixels - array[:,1].size % number_of_pixels), 'constant')

    # Reshape the array into a 2D array with the specified number of columns
    lineScanSummed = lineScanSummed.reshape(-1, number_of_pixels)

    # Get the length of the columns
    interval = lineScanSummed.shape[0]

    # Sum the columns
    lineScanSummed = lineScanSummed.sum(axis=0)

    # Initialize the NP detections array (in one line scan)
    detectionsLineScan = np.zeros((regions.shape[0], 2))

    # Store the start indeces of each peak in the line scan
    detectionsLineScan[:, 0] = regions[:, 0]
    detectionsLineScan[:, 1] = detections

    # Determine the pixel number for each detection
    detectionsLineScan[:, 0] = detectionsLineScan[:, 0] // interval

    # Create a copy of lineScanSummed for the background calculation
    lineScanSummedBackground = lineScanSummed.copy()

    # Subtract the NP signal from the corresponding pixels
    lineScanSummedBackground[detectionsLineScan[:, 0].astype(int)] -= detectionsLineScan[:, 1]

    return (detectionsLineScan, lineScanSummed, lineScanSummedBackground)

    
# Read the file into a numpy array
array = np.genfromtxt(file_path, delimiter=',', skip_header=4, skip_footer=3)
# filtered_array = signal.medfilt(array[:, 1], 51)

# if np.mean(filtered_array) < 10:
#     epsilon = 0.5
#     print('epsilon = 0.5')
# else:
#     epsilon = 0
#     print('epsilon = 0')

# Sc, Sd = poisson.currie(filtered_array, epsilon=epsilon)

# detections1, labels1, regions1 = detection.accumulate_detections(array[:,1], Sc, Sd, integrate=True)

# Call the process_file function
detectionsLineScan, lineScanSummed, lineScanSummedBackground = process_file(file_path, convertToCounts=False, gas_blank_start=0, gas_blank_end=1, number_of_pixels=20)

# Crop the array. Remove the top 4 rows and the bottom 3 rows
# array = array[4:-3,:]

# plt.plot(array[:, 0], array[:, 1])
# #plt.plot(Sc, 'r--')
# #plt.plot(Sd, 'g--')
# plt.plot(array[regions[:, 0], 0], array[regions[:, 0], 1], 'ro')
# plt.plot(array[regions[:, 1], 0], array[regions[:, 1], 1], 'go')
# plt.legend(['Raw Data', 'Filtered Data', 'Sc', 'Sd', 'Start', 'End'])
# plt.show()

# print("Detections:", detections)
# print("Regions:", regions)

print(np.shape(detectionsLineScan))
print(np.shape(lineScanSummed))
print(np.shape(lineScanSummedBackground))

# Create a 