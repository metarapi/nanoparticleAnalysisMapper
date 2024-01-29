import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# linescan = np.load('C:/Users/gala_/Documents/Coding/NPAnalysisMapper-main/mysite/generated/linescan_150.csv.npy')

# plt.plot(linescan)
# plt.show()

probabilityMap = pd.read_csv("C:/Users/gala_/Documents/Coding/NPAnalysisMapper-main/mysite/probabilityMap.csv")
probabilityMap = np.array(probabilityMap)

print(np.shape(probabilityMap))

smallerMap = probabilityMap[100:250,100:250]

print(np.size(probabilityMap,0))

plt.imshow(smallerMap)
plt.show()