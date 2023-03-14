import torch
import numpy as np
from onshapeInterface.ConfigurationEncoder import KinematicSampleConfigurationEncoder, ValueWithUnit, Units
from data.DataFromCsv import DataFromCsv
from data.VisualizeData import visualizeData
from data.Data import Data

dataExporter = DataFromCsv("ihmcSpine_Reparameterized")
loadedData = dataExporter.loadData()
visualizeData(loadedData)
