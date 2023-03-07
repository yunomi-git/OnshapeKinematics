import json

import torch
from onshapeComm.OnshapeAPI import OnshapeAPI

from onshapeComm.ConfigurationEncoder import ValueWithUnit, Units
from onshapeComm.Keys import Keys
from onshapeComm.RequestUrlCreator import RequestUrlCreator

from ihmcSpine.SpineCostEvaluator import SpineCostEvaluator
from optimization.BayesOptWrapper import BayesOptOnshapeWrapper

access = 'I6M5WhNnlnrPeGGFucyKwlwa'
secret = 'W9qbMjKaYzfBRbg8MPoAuP7sDICkLhlByVYLAT8cehiF4Gbv'
keys = Keys(access, secret)
url = "https://cad.onshape.com/documents/c6a60909a9693027fe5bb9e9/w/50fafe234fce490c861a55b4/e/917b3052222d7c5ffe909970"

requestUrlCreator = RequestUrlCreator(url)
onshapeAPI = OnshapeAPI(keys, requestUrlCreator)


weights = [0.2, 0.2, 0.2]
spineCostEvaluator = SpineCostEvaluator()
def ankleCostTo1D(parameters, apiResponse):
    costs = SpineCostEvaluator.calculateCostFromOnshape(parameters, apiResponse)
    costs.print()
    if costs.parametersAreInvalid():
        oneDCost = -1.0
    else:
        oneDCost = (-costs.forwardSweep * weights[0] / 3.0 +
                    -costs.sideSweep * weights[0] / 4.0 +
                    -costs.pitchForwardMaxRoll * weights[1] / 60.0 +
                    -costs.pitchForward0ROll * weights[1] / 60.0 +
                    costs.torque * weights[2] / 500.0)
    print("1 d cost: ")
    print(oneDCost)
    return oneDCost

if __name__ == "__main__":
    unitsList = [Units.DEGREE, Units.METER, Units.DEGREE, Units.METER, Units.DEGREE]
    onshapeCostEvaluator = spineCostEvaluator.calculateCostFromOnshape
    bayesOptKinematicWrapper = BayesOptOnshapeWrapper(onshapeCostEvaluator=onshapeCostEvaluator,
                                                      onshapeAPI=onshapeAPI,
                                                      parameterDimensions=len(unitsList),
                                                      unitsList=unitsList)
    # TODO: also options to load past data, select specific points to sample
    bestParam, bestCost = bayesOptKinematicWrapper.optimize(initialPoints=4,
                                                            numIterations=20,
                                                            boundsMagnitude=0.03)
    # TODO: also select where to save this run

    print("Best Parameters")
    print(bestParam)
    bayesOptKinematicWrapper.evaluateCostWrapper(bestParam)
    print("Original Parameters")
    bayesOptKinematicWrapper.evaluateCostWrapper(torch.tensor([0,0,0,0,0]))