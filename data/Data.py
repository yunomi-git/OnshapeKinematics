# Stores a collection of X and Y values
import numpy as np
import torch

class Data:
    def __init__(self,
                 initialXValues : torch.Tensor = None,
                 initialYValues : torch.Tensor = None):
        if (initialXValues is None) or (initialYValues is None):
            self.yValues = torch.tensor([[]])
            self.xValues = torch.tensor([[]])
        else:
            self.xValues = initialXValues
            self.yValues = initialYValues

    def getAllXTensor(self) -> torch.Tensor:
        return self.xValues

    def getAllYTensor(self):
        return self.yValues

    def addDataFromNumpy(self,
                         numpyX : np.ndarray,
                         numpyY : np.ndarray):
        tensorX = torch.from_numpy(numpyX).double()
        tensorY = torch.from_numpy(numpyY).double()
        self.addDataFromTensor(tensorX, tensorY)

    def addDataFromTensor(self,
                          tensorX: torch.Tensor,
                          tensorY: torch.Tensor):
        self.yValues = self.addDataToList(self.yValues, tensorY)
        self.xValues = self.addDataToList(self.xValues, tensorX)


    def addDataToList(self, tensorList : torch.Tensor, tensorVal : torch.Tensor):
        newVal = torch.reshape(tensorVal, (1, tensorVal.numel()))
        if torch.numel(tensorList) == 0:
            return newVal

        return torch.cat((tensorList, newVal), dim=0)