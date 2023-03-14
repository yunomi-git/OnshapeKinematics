# Data is collection of inputs x and outputs y.
# Converts between a tensor of inputs and a csv
import os.path

import torch
from typing import Tuple
import pandas as pd
import paths

from storage.Data import Data

class DataFromCsv:
    def __init__(self, fileName : str):
        self.numpy_dtype = 'float32'
        if not os.path.isdir(paths.DATA_DIR):
            os.makedirs(paths.DATA_DIR)
        self.dataInputPath = paths.createPathToCsvDataFile(fileName, isInputs=True)
        self.dataOutputPath = paths.createPathToCsvDataFile(fileName, isInputs=False)

    def saveData(self, data : Data):
        xTensor = data.getAllXTensor()
        yTensor = data.getAllYTensor()
        xDataFrame = pd.DataFrame(xTensor.numpy())
        yDataFrame = pd.DataFrame(yTensor.numpy())
        xDataFrame.to_csv(path_or_buf=self.dataInputPath, index=False)
        yDataFrame.to_csv(path_or_buf=self.dataOutputPath, index=False)

    # Output is (xTensor, yTensor)
    def loadData(self) -> Data:
        if (not os.path.isfile(self.dataInputPath)) or (not os.path.isfile(self.dataOutputPath)):
            return None

        xDataFrame = pd.read_csv(self.dataInputPath)
        yDataFrame = pd.read_csv(self.dataOutputPath)

        xTensor = torch.Tensor(xDataFrame.to_numpy(dtype=self.numpy_dtype))
        yTensor = torch.Tensor(yDataFrame.to_numpy(dtype=self.numpy_dtype))

        return Data(initialXValues=xTensor, initialYValues=yTensor)