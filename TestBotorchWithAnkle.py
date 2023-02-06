import torch
from botorch.models import SingleTaskGP
from botorch.fit import fit_gpytorch_mll
from gpytorch.mlls import ExactMarginalLogLikelihood
from botorch.acquisition import UpperConfidenceBound
from botorch.optim import optimize_acqf
import time

from onshapeComm.OnshapeAPI import OnshapeAPI

from onshapeComm.ConfigurationEncoder import ValueWithUnit, Units
from onshapeComm.Keys import Keys
from onshapeComm.RequestUrlCreator import RequestUrlCreator
import onshapeComm.Names as Names
from ihmcAnkle.AnkleConfiguration import AnkleConfiguration
from ihmcAnkle.AnkleCost import AnkleCostEvaluator, AnkleCosts

access = 'I6M5WhNnlnrPeGGFucyKwlwa'
secret = 'W9qbMjKaYzfBRbg8MPoAuP7sDICkLhlByVYLAT8cehiF4Gbv'
keys = Keys(access, secret)
url = "https://cad.onshape.com/documents/6b351a18863dce94af4a4571/w/024504447ddcbbc5882aae07/e/3040b95620727a4e88cf17dd"

requestUrlCreator = RequestUrlCreator(url)
onshapeAPI = OnshapeAPI(keys, requestUrlCreator)

weights = [0.2, 0.2, 0.2]
def appendNewCost(costList, newCost):
    # costlist is 1xn tensor
    # newCost is scalar cost
    tensorCost = torch.tensor([newCost]).double()
    costList = torch.cat((costList, tensorCost), dim=0)
    return costList

def ankleTo1DCost(costs : AnkleCosts, weights):
    oneDCost = (-costs.forwardSweep * weights[0] +
             -costs.sideSweep * weights[0] +
             -costs.pitchForwardMaxRoll * weights[1] +
             -costs.pitchForward0ROll * weights[1] +
             costs.torque * weights[2])
    return oneDCost

def costFunction(parameters):
    # costs = costFunctionMultiD(parameters)
    # oneDCost = ankleTo1DCost(costs, weights)
    oneDCost = 1
    return oneDCost

def costFunctionMultiD(parameters):
    print(parameters)
    numpyParam = parameters.numpy()
    configuration = AnkleConfiguration()
    configuration.setNewConfiguration(globalX=ValueWithUnit(numpyParam[0], Units.METER),
                                      globalY=ValueWithUnit(numpyParam[1], Units.METER),
                                      globalZ=ValueWithUnit(numpyParam[2], Units.METER),
                                      relativeX=ValueWithUnit(numpyParam[3], Units.METER),
                                      relativeY=ValueWithUnit(numpyParam[4], Units.METER),
                                      relativeZ=ValueWithUnit(numpyParam[5], Units.METER))

    tic = time.perf_counter()
    apiResponse = onshapeAPI.doAPIRequestForJson(configuration, Names.SAMPLES_ATTRIBUTE_NAME)
    toc = time.perf_counter()
    print("time total " + str(toc - tic))

    costs = AnkleCostEvaluator.calculateCostFromOnshape(configuration, apiResponse)
    costs.print()
    return costs


numStartingData = 4
searchDims = 6
boundMag = 0.03
train_X = ((2 * torch.rand(numStartingData, searchDims) - 1.0) * boundMag).double() # in meters
train_Y = torch.tensor([[]])
for i in range(numStartingData):
    newY = costFunction(train_X[i])
    print(newY)
    print(train_Y)
    train_Y = appendNewCost(train_Y, newY)
# train_Y = torch.reshape(train_Y, (numStartingData, 1))
bounds = torch.stack([torch.ones(searchDims) * -boundMag, torch.ones(searchDims) * boundMag]).double()

for i in range(10):
    gp = SingleTaskGP(train_X, train_Y)
    mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
    fit_gpytorch_mll(mll);

    UCB = UpperConfidenceBound(gp, beta=0.1)

    candidate, acq_value = optimize_acqf(
        UCB, bounds=bounds, q=1, num_restarts=5, raw_samples=20,
    )

    train_X = torch.cat((train_X, candidate))
    newY = costFunction(candidate[0])
    print(newY)
    print(train_Y)
    train_Y = appendNewCost(train_Y, newY)
    print("------------")

bestIndex = torch.argmax(train_Y)
bestParam = train_X[bestIndex]
bestCosts = costFunctionMultiD(bestParam)
originalCosts = costFunctionMultiD([0,0,0,0,0,0])

print("Best Costs:")
bestCosts.print()

print("Original Costs:")
originalCosts.print()