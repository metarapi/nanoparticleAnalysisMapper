# import numpy as np

# columns = 2

# # Create the initial 1D array
# arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# # Pad the arr with zeros so that it can be reshaped into a 2D array with two columns
# arr = np.pad(arr, (0, columns - arr.size % columns), 'constant')

# # Reshape it into a 2D array with two columns and grouping elements by pairs
# reshaped_arr = arr.reshape(-1, columns)



# print(reshaped_arr)

# sum_of_columns = reshaped_arr.sum(axis=0)

# print(sum_of_columns)

# import numpy as np

# original_vector = np.array([1, 5, 999, 1000, 1001, 1250, 1999, 2000, 2400])

# # Define the interval
# interval = 1000

# # Divide the original vector by the interval and take the integer part
# new_vector = original_vector // interval

# # Add 1 to the new_vector to start the count from 1
# new_vector += 1

# print(new_vector)

import numpy as np
import plotly.graph_objects as go
import plotly.express as px

data = np.load('D:/DjangoCoding/NPAnalysisMapper/mysite/media/datasets/numpy_files/Dino1.npz')

# Access arrays
summedMap = data['summedMap']
backgroundMap = data['backgroundMap']
detectionsList = data['detectionsList']
npTotalMap = data['npTotalMap']

print(np.shape(detectionsList))

# Use imshow to plot the summed map
fig = px.imshow(npTotalMap)
fig.show()