import json

import torch
from onshapeComm.OnshapeAPI import OnshapeAPI

from onshapeComm.ConfigurationEncoder import ValueWithUnit, Units
from onshapeComm.Keys import Keys
from onshapeComm.RequestUrlCreator import RequestUrlCreator

from ihmcAnkle.AnkleCost import AnkleCostEvaluator, AnkleCosts
from optimization.BayesOptWrapper import BayesOptOnshapeWrapper

access = 'I6M5WhNnlnrPeGGFucyKwlwa'
secret = 'W9qbMjKaYzfBRbg8MPoAuP7sDICkLhlByVYLAT8cehiF4Gbv'
keys = Keys(access, secret)
url = "https://cad.onshape.com/documents/6b351a18863dce94af4a4571/w/024504447ddcbbc5882aae07/e/3040b95620727a4e88cf17dd"

requestUrlCreator = RequestUrlCreator(url)
onshapeAPI = OnshapeAPI(keys, requestUrlCreator)

weights = [0.2, 0.2, 0.2]

def ankleCostTo1D(parameters, apiResponse):
    costs = AnkleCostEvaluator.calculateCostFromOnshape(parameters, apiResponse)
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

unitsList = [Units.METER, Units.METER, Units.METER, Units.METER, Units.METER, Units.METER]
onshapeCostEvaluator = ankleCostTo1D
bayesOptKinematicWrapper = BayesOptOnshapeWrapper(onshapeCostEvaluator=onshapeCostEvaluator,
                                                  onshapeAPI=onshapeAPI,
                                                  parameterDimensions=6,
                                                  unitsList=unitsList)
bestParam, bestCost = bayesOptKinematicWrapper.optimize(initialPoints=4,
                                                        numIterations=20,
                                                        boundsMagnitude=0.03)

print("Best Parameters")
print(bestParam)
bayesOptKinematicWrapper.evaluateCostWrapper(bestParam)
print("Original Parameters")
bayesOptKinematicWrapper.evaluateCostWrapper(torch.tensor([0,0,0,0,0,0]))

