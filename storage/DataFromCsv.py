# Data is collection of inputs x and outputs y.
# Converts between a tensor of inputs and a csv
import torch
from typing import Tuple
import pandas as pd

class DataFromCsv:
    def __init__(self, filePath : str):
        dataInputSuffix = "_input"
        dataOutputSuffix = "_output"

        self.dataInputPath = filePath + dataInputSuffix
        self.dataOutputPath = filePath + dataOutputSuffix

    def saveData(self, xTensor : torch.Tensor, yTensor : torch.Tensor):
        pass


    def loadData(self) -> Tuple[torch.Tensor, torch.Tensor]:
        pass