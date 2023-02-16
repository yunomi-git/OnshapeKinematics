import numpy as np
from abc import ABC, abstractmethod
from onshapeComm.ConfigurationEncoder import KinematicSampleConfigurationEncoder

class OnshapeCostEvaluator:
    def getCost(self, parameters : np.ndarray, apiResponse : dict):
        pass