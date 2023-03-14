# Stores a collection of X and Y values
import numpy as np
import torch

class Data:
    def __init__(self):
        self.yValues = torch.tensor([[]])
        self.xValues = torch.tensor([[]])

    def getAllXTensor(self):
        return self.xValues

    def getAllYTensor(self):
        return self.yValues

    def addDataFromNumpy(self, numpyX : np.ndarray = None,
                numpyY : np.ndarray = None):
        tensorX = torch.from_numpy(numpyX).double()
        tensorY = torch.from_numpy(numpyY).double()
        self.addDataFromTensor(tensorX, tensorY)

    def addDataFromTensor(self, tensorX: torch.Tensor = None,
                         tensorY: torch.Tensor = None):
        self.yValues = self.addDataToList(self.yValues, tensorY)
        self.xValues = self.addDataToList(self.xValues, tensorX)

    def addDataToList(self, tensorList : torch.Tensor, tensorVal : torch.Tensor):
        newVal = torch.reshape(tensorVal, (1, tensorVal.numel()))
        if torch.numel(tensorList) == 0:
            return newVal

        return torch.cat((tensorList, newVal), dim=0)