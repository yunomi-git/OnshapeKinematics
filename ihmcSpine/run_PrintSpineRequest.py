import math
import matplotlib.pyplot as plt

from onshapeInterface.OnshapeAPI import OnshapeAPI
from mathUtil.kinematics import KinematicsToolbox, Unit
import numpy as np
import time
import json
import ihmcSpine.SpineNames as SpineNames

from onshapeInterface.ConfigurationEncoder import KinematicSampleConfigurationEncoder, ValueWithUnit, Units
from onshapeInterface.Keys import Keys
from onshapeInterface.RequestUrlCreator import RequestUrlCreator
import onshapeInterface.Names as Names
from onshapeInterface.JsonParser import JsonToPython
from ihmcSpine import SpineCostEvaluator
from ihmcSpine.SpineVisualization import plotTorques




if __name__ == "__main__":
    access = 'I6M5WhNnlnrPeGGFucyKwlwa'
    secret = 'W9qbMjKaYzfBRbg8MPoAuP7sDICkLhlByVYLAT8cehiF4Gbv'
    keys = Keys(access, secret)
    url = "https://cad.onshape.com/documents/c6a60909a9693027fe5bb9e9/w/50fafe234fce490c861a55b4/e/917b3052222d7c5ffe909970"

    requestUrlCreator = RequestUrlCreator(url)
    onshapeAPI = OnshapeAPI(keys, requestUrlCreator)

    unitsList = [Units.RADIAN,
                 Units.METER,
                 Units.RADIAN,
                 Units.METER,
                 Units.METER]

    numpyParameters = np.array([0.1745,  0.060,  0.611,  0.200,  0.020])
    parameters = KinematicSampleConfigurationEncoder(unitsList=unitsList, numpyParameters=numpyParameters)

    # parameters.addParameters(np.array([0.10,  # Crank Angle
    #                                          0.055, # Crank Length
    #                                          0.30, # Mounting Angle
    #                                          0.10, # Mounting Length
    #                                          0.02])) # Bore Diameter
    print(parameters.getEncoding())

    tic = time.perf_counter()
    apiResponse = onshapeAPI.doAPIRequestForJson(parameters, Names.SAMPLES_ATTRIBUTE_NAME)
    toc = time.perf_counter()

    print(json.dumps(apiResponse, indent=4))
    print("time total " + str(toc - tic))

    minTorqueConstraint = 150.0
    actuatorExtraLength = 0.063

    costs = SpineCostEvaluator.getSpineCostsNd(apiResponse,
                                               parameters=parameters.numpyParameters,
                                               minTorqueConstraint=minTorqueConstraint,
                                               actuatorExtraLength=actuatorExtraLength,
                                               boreDiameterOverride=True,
                                               debug=True)
    costs.print()

    weights = {
        SpineNames.MaxWidthCost : 0.2,
        SpineNames.MaxHeightCost : 0.2,
        SpineNames.MaxForceCost : 0.3,
        SpineNames.BoreDiameterCost : 0.1
    }

    normalization = {
        SpineNames.MaxWidthCost: 0.05,
        SpineNames.MaxHeightCost: 0.14,
        SpineNames.MaxForceCost: 6000.0,
        SpineNames.BoreDiameterCost: 0.02
    }
    costEvaluator = SpineCostEvaluator.SpineCostEvaluator(weights=weights,
                                                          normalization=normalization,
                                                          minTorqueConstraint=minTorqueConstraint,
                                                          actuatorExtraLength=actuatorExtraLength)
    cost1D = costEvaluator.calculateCostFromOnshape(parameters=parameters.numpyParameters,
                                                    apiResponse=apiResponse)
    print("1d cost: " + str(cost1D))

    plotTorques(apiResponse, SpineCostEvaluator.getBoreDiameter(parameters.numpyParameters))





# print(json.dumps(costs.objectiveCosts, indent=4))

