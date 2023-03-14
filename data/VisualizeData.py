# Use these methods to show what is getting sampled by the optimizer
from data.Data import Data
import matplotlib.pyplot as plt

def visualizeData(data : Data):
    xData = data.getAllXTensor()
    xDimensions = xData.size(dim=1)
    numData = xData.size(dim=0)

    fig1, axs1 = plt.subplots(xDimensions)
    fig1.suptitle('Data')
    for i in range(xDimensions):
        axs1[i].scatter(range(numData), xData[:, i])

    fig2, axs2 = plt.subplots()
    fig2.suptitle('Combined Data')
    for i in range(xDimensions):
        axs2.scatter(range(numData), xData[:, i])

