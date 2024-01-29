import numpy as np
import pandas as pd
import scipy.signal as signal
import os
from .poisson import currie
from .detection import accumulate_detections
from django.conf import settings
from django.core.cache import cache

import aiofiles
import asyncio
# from django_eventstream import send_event


def process_file(
    file_path,
    file_number,
    total_files, 
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
    Sc, Sd = currie(filtered_array, epsilon=epsilon)

    # Use the Sc and Sd values to detect the peaks in the data
    detections, labels, regions = accumulate_detections(array[:,1], Sc, Sd, integrate=True)

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

    progress = (file_number / total_files) * 100
    cache.set('process_progress', progress)
    return (detectionsLineScan, lineScanSummed, lineScanSummedBackground)

def process_data(
    experiment, 
    experiment_folder, 
    numpy_file, 
    cal_curve,
    slope,
    intercept,
    np_size,
    signal_median,
    convert_to_cps=True,
    gas_blank_start=0,
    gas_blank_end=0,
    number_of_pixels=20):

    # Create a list of all the files in the experiment folder
    absolute_experiment_folder = os.path.join(settings.MEDIA_ROOT, experiment_folder)
    files = os.listdir(absolute_experiment_folder)
    
    # Sort the files in the experiment folder
    files.sort()

    # Determine the number of files in the experiment folder
    number_of_files = len(files)

    # Initialize the output summed map array, and the the output background array
    summedMap = np.empty((number_of_files, number_of_pixels))
    backgroundMap = np.empty((number_of_files, number_of_pixels))

    # Initialize the output detectionsList list
    detectionsList = []

    # Initialize the current file number
    file_number = 0

    # Loop over each file in the experiment folder
    for file_name in files:

        # Process the current file
        file_path = os.path.join(absolute_experiment_folder, file_name)

        file_number += 1

        detectionsLineScan, lineScanSummed, lineScanSummedBackground = process_file(file_path, 
            convertToCounts=convert_to_cps, 
            gas_blank_start=gas_blank_start, 
            gas_blank_end=gas_blank_end, 
            number_of_pixels=number_of_pixels,
            file_number=file_number,
            total_files=number_of_files)

        # Populate the line scan summed map array and background array
        summedMap[files.index(file_name), :] = lineScanSummed
        backgroundMap[files.index(file_name), :] = lineScanSummedBackground

        # Create a vector of the file index for each detection in a line scan
        lineScanVector = np.ones((detectionsLineScan.shape[0], 1)) * files.index(file_name)

        # Add an additional column to the detectionsLineScan array to store the file index
        detectionsLineScan = np.append(detectionsLineScan, lineScanVector, axis=1)

        # Append the detectionsLineScan array to the detectionsList list
        detectionsList.append(detectionsLineScan)
    
    # Convert the detectionsMap list to a numpy array (keeping the same number of columns)
    detectionsList = np.vstack(detectionsList)

    # Calibrate the detectionsList array to convert the second column from counts to NP size

    if cal_curve:
        for i in range(detectionsList.shape[0]):
            detectionsList[i,1] = (detectionsList[i,1]**(1./3.))*slope + intercept
    else:
        for i in range(detectionsList.shape[0]):
            detectionsList[i,1] = ((detectionsList[i,1]**(1./3.))*np_size)/signal_median

    # Create an image for the total number of NPs in each pixel
    npTotalMap = np.zeros((number_of_files, number_of_pixels))

    # Convert the relevant columns to integers
    x = detectionsList[:, 0].astype(int)
    y = detectionsList[:, 2].astype(int)

    # Use advanced indexing to increment the relevant cells
    np.add.at(npTotalMap, (x, y), 1)

    # Create a series of NP maps segregated by size in steps of 10 nm
    
    size_ranges = [(0, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90), (90, 100), (100, float('inf'))]

    # Create a list to store numpy arrays for each size range
    filtered_maps_list = []

    # Loop over each size range
    for size_range in size_ranges:
        # Filter the data to only include NPs in the current size range
        filtered_data = detectionsList[(detectionsList[:, 1] >= size_range[0]) & (detectionsList[:, 1] < size_range[1])]

        # Create an image for the total number of NPs in each pixel
        x = filtered_data[:, 0].astype(int)
        y = filtered_data[:, 2].astype(int)
        filtered_map = np.zeros((number_of_files, number_of_pixels))
        np.add.at(filtered_map, (x, y), 1)

        # Append the filtered data to the filtered_data_list
        filtered_maps_list.append(filtered_map)

    # Save the output data to a .npz file
    absolute_numpy_file = os.path.join(settings.MEDIA_ROOT, numpy_file)
    np.savez(absolute_numpy_file, summedMap=summedMap, backgroundMap=backgroundMap, detectionsList=detectionsList, npTotalMap=npTotalMap, *filtered_maps_list)

    return summedMap, backgroundMap, detectionsList, npTotalMap