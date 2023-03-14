import numpy as np
from abc import ABC, abstractmethod
from onshapeInterface.ConfigurationEncoder import KinematicSampleConfigurationEncoder

class OnshapeCostEvaluator:
    def getCost(self, parameters : np.ndarray, apiResponse : dict):
        pass