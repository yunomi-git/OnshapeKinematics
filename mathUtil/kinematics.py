import numpy as np

from enum import Enum
class Unit(Enum):
    LENGTH=1
    ANGLE=2

class KinematicsToolbox:
    def __init__(self, inputUnits, outputDim, kinematicsCalculator):
        self.inputDim = len(inputUnits)
        self.inputUnits = []
        for i in range(self.inputDim):
            if inputUnits[i] == Unit.LENGTH:
                self.inputUnits.append("m")
            else:
                self.inputUnits.append("deg")
        self.outputDim = outputDim
        self.kinematicsCalculator = kinematicsCalculator

    # Inputs is a numpy array
    def calculateKinematics(self, inputs):
        return self.kinematicsCalculator(inputs, self.inputUnits)

    # Inputs and output is a numpy array
    def calculateJacobian(self, inputs, stepSizes):
        jacobian = np.zeros([self.inputDim, self.outputDim])

        originalOutput = self.calculateKinematics(inputs)
        for i in range(self.inputDim):
            stepSize = stepSizes[i]
            perturbedInput = np.copy(inputs)
            perturbedInput[i] += stepSize

            perturbedOutput = self.calculateKinematics(perturbedInput)
            gradient = np.subtract(perturbedOutput, originalOutput) / stepSize 
            jacobian[:,i] = gradient
        
        return jacobian



