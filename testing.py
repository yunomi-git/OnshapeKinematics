import torch
import numpy as np
from onshapeInterface.ConfigurationEncoder import KinematicSampleConfigurationEncoder, ValueWithUnit, Units
from storage.DataFromCsv import DataFromCsv
from storage.Data import Data

data = Data()
data.addDataFromNumpy(np.array([1.0, 3.0, 2.0]), np.array([2.0, 3.0]))
data.addDataFromNumpy(np.array([2.0, 7.0, 4.0]), np.array([4.0, 6.0]))
data.addDataFromNumpy(np.array([1.2, 3.2, 2.3]), np.array([2.3, 3.1]))

dataExporter = DataFromCsv("testing")
dataExporter.saveData(data)
loadedData = dataExporter.loadData()
print()