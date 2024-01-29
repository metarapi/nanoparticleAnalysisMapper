import numpy as np
import pandas as pd
import scipy.signal as signal
import matplotlib.pyplot as plt

# Maximum number of nanoparticles expected per pixel
baselineProbability = 25
# Flicker noise (%)
flickerNoise = 0.05
# Background signal intesity (counts)csv
backgroundSignal = 3
# Single NP signal average:
singleNP = 50
# Nanoparticle distribution sigma (spread)
sigma = 0.5
# Single pixel time (in multiples of 100us)
pixelTime = 2500 # 25 ms pixel

probabilityMap = pd.read_csv("D:/DjangoCoding/NPAnalysisMapper/mysite/probabilityMap.csv")
probabilityMap = np.array(probabilityMap)
probabilityMap = probabilityMap[100:250,100:250]


mapSizeX = np.size(probabilityMap,0)
mapSizeY = np.size(probabilityMap,1)

# Flicker noise map
flickerNoiseMap = (np.random.rand(mapSizeX,mapSizeY)*flickerNoise)-flickerNoise/2

# NP Baseline Total Number Map
npBaselineMap = np.ones((mapSizeX,mapSizeY))*baselineProbability

# NP Total Number Map. This map holds the number of NPs in each pixel.
npTotalNumberMap = np.round((flickerNoiseMap + probabilityMap) * npBaselineMap)

# Remove negative values
npTotalNumberMap[npTotalNumberMap < 0] = 0

# Single NP convolution kernel
npKernel = np.array([0.05, 0.2, 0.55, 0.15, 0.05])

npMap = []

for row in range(mapSizeX):
    if row == 100:
        return
    print('Generating line scan '+ str(row+1))
    lineScan = np.empty((1,1))
    
    for column in range(mapSizeY):
        npNum = int(npTotalNumberMap[row,column])
        singlePixelSignal = np.zeros((1,pixelTime))
        singlePixelSignal[0,np.random.randint(0,pixelTime,npNum)] += singleNP
        lineScan = np.append(lineScan,singlePixelSignal)

    lineScan = signal.fftconvolve(lineScan,npKernel)
    timeAxis = np.linspace(1,np.size(lineScan,0),np.size(lineScan,0))
    lineScan = np.append(lineScan,timeAxis,axis=0)
    
    filename = f'generated/linescan_{str(row).zfill(3)}.csv'
    np.savetxt(filename, lineScan, delimiter=',')
    
    #npMap.append(lineScan)

# print(np.shape(npMap))

# npMap = np.vstack(npMap)

# print(np.shape(npMap))

# #backgroundSignalMap = np.ones((np.size(npMap,1),np.size(npMap,2)))*backgroundSignal



# # This will be added to the total signal
# # backgroundSignalMap = np.ones((mapSizeX,mapSizeY))*backgroundSignal

# #array[np.random.randint(0,1000,10),1] += np.random.randint(10,100,10)

# print(type(npMap))

# np.save('npMap',npMap)

# plt.imshow(npTotalNumberMap)

# plt.show()