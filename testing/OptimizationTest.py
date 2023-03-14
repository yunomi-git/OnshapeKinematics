from onshapeInterface.OnshapeKinematics import OnshapeKinematicsAPI
from mathUtil.kinematics import KinematicsToolbox, Unit
import numpy as np
import time
from optimization.Optimizer import GradientDescentOptimizer, GDOptimizationParameters, OptimizationEndConditions
from optimization.CostEvaluator import CostEvaluator

# Document is https://cad.onshape.com/documents/e78b514b41a6ecf3294c8a73/w/947827fa01808e74d00babf4/e/273c0fd3e7a3f8c057ea3fc1
access = 'Eiu0FEHRtfHMUd8e3dovW6wR'
secret = 'YmluDgPnCePqppY6xPnH2hOhtN6nhT3R4Mwus6Cc7CJQDFSk'
docID = "e78b514b41a6ecf3294c8a73"
workspaceID = "947827fa01808e74d00babf4"
elementID = "273c0fd3e7a3f8c057ea3fc1"

numInputs = 2
numOutputs = 2
inputUnits = [Unit.LENGTH, Unit.LENGTH]
onshapeAPI = OnshapeKinematicsAPI(access, secret, docID, workspaceID, elementID, numInputs)
kinematicsToolbox = KinematicsToolbox(inputUnits, numOutputs, onshapeAPI.getOutputKinematics)

optimizerParameters = GDOptimizationParameters(
    optimizationStepSize=0.01,
    gradientStepFactor=0.01,
    optimizationStepSizeScaling=1.0,
    scaleEveryNSteps=1,
    weightedScaling=np.array([0.7, 0.7])
    )

endConditions = OptimizationEndConditions(
    maxSteps=40,
    convergenceThreshold=0.0001
)

initialValue = np.array([0.4, 0.8])
class DistanceCostEvaluator(CostEvaluator):
    def __init__(self):
        super(DistanceCostEvaluator, self).__init__()
        self.desired = np.array([0.6, 0.7])

    def getCost(self, value):
        output = kinematicsToolbox.calculateKinematics(value)
        return np.linalg.norm(np.subtract(output, self.desired))

costEvaluator = DistanceCostEvaluator()
optimizer = GradientDescentOptimizer(initialValue, costEvaluator, optimizerParameters)
tic = time.perf_counter()
optimizer.optimizeUntilEndCondition(endConditions)
toc = time.perf_counter()
print("time " + str(toc - tic))

state, cost = optimizer.getCurrentStateAndCost()
print(state)


# inputs = np.array([0.20, 0.30])

# tic = time.perf_counter()
# outputs = kinematicsToolbox.calculateKinematics(inputs)
# toc = time.perf_counter()
# print(outputs)
# print("time " + str(toc - tic))

# stepSizes = np.array([0.001, 0.001])
# tic = time.perf_counter()
# outputs = kinematicsToolbox.calculateJacobian(inputs, stepSizes)
# toc = time.perf_counter()
# print(outputs)
# print("time " + str(toc - tic))


