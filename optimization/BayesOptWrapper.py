import torch
from botorch.models import SingleTaskGP
from botorch.fit import fit_gpytorch_mll
from gpytorch.mlls import ExactMarginalLogLikelihood
from botorch.acquisition import UpperConfidenceBound
from botorch.optim import optimize_acqf

from optimization import OnshapeCostEvaluator
from onshapeComm.ConfigurationEncoder import KinematicSampleConfigurationEncoder
from onshapeComm.OnshapeAPI import OnshapeAPI
import onshapeComm.Names as Names
import time
from onshapeComm.ConfigurationEncoder import ValueWithUnit, Units
def appendNew1DCost(costList, newCost):
    # costlist is 1xn tensor
    # newCost is scalar cost
    tensorCost = torch.tensor([[newCost]]).double()

    if torch.numel(costList) == 0:
        return tensorCost

    costList = torch.cat((costList, tensorCost), dim=0)
    return costList
class BayesOptOnshapeWrapper:
    def __init__(self, onshapeCostEvaluator : OnshapeCostEvaluator, onshapeAPI : OnshapeAPI, parameterDimensions, unitsList):
        self.onshapeAPI = onshapeAPI
        self.onshapeCostEvaluator = onshapeCostEvaluator
        self.parameterDimensions = parameterDimensions
        self.unitsList = unitsList

    def optimize(self, initialPoints, numIterations, boundsMagnitude):
        # Initial Sampling
        bounds = torch.stack([torch.ones(self.parameterDimensions) * -boundsMagnitude,
                              torch.ones(self.parameterDimensions) * boundsMagnitude]).double()
        train_X = ((2 * torch.rand(initialPoints, self.parameterDimensions) - 1.0) * boundsMagnitude).double()  # in meters
        originalX = torch.zeros(1, self.parameterDimensions)
        train_X = torch.cat((originalX, train_X))
        train_Y = torch.tensor([[]])
        for i in range(initialPoints + 1):
            newY = self.evaluateCostWrapper(train_X[i])
            train_Y = appendNew1DCost(train_Y, newY)
            print("---------------------------------------")

        # Actually Run
        for i in range(numIterations):
            gp = SingleTaskGP(train_X, train_Y)
            mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
            fit_gpytorch_mll(mll);

            UCB = UpperConfidenceBound(gp, beta=0.5)

            candidate, acq_value = optimize_acqf(
                UCB, bounds=bounds, q=1, num_restarts=5, raw_samples=20,
            )

            train_X = torch.cat((train_X, candidate))
            newY = self.evaluateCostWrapper(candidate[0])
            print(newY)
            train_Y = appendNew1DCost(train_Y, newY)
            print("---------------------------------------")

        bestIndex = torch.argmax(train_Y)
        bestParam = train_X[bestIndex]
        bestCost = self.evaluateCostWrapper(bestParam)
        print("All Costs: ------------")
        print(train_Y)
        print("---------------")
        return bestParam, bestCost

    def evaluateCostWrapper(self, parameters : torch.Tensor):
        configuration = KinematicSampleConfigurationEncoder()
        numpyParameters = parameters.numpy()
        print(numpyParameters)

        for i in range(self.parameterDimensions):
            value = numpyParameters[i]
            unit = self.unitsList[i]
            configuration.addParameter(ValueWithUnit(value, unit))

        tic = time.perf_counter()
        apiResponse = self.onshapeAPI.doAPIRequestForJson(configuration, Names.SAMPLES_ATTRIBUTE_NAME)
        toc = time.perf_counter()
        print("time total " + str(toc - tic))


        cost = self.onshapeCostEvaluator(numpyParameters, apiResponse)
        return cost

