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
    url = "https://cad.onshape.com/documents/07c87d36d9881deeeea3d0c5/w/a5fc87e91bbbedea94bb5b58/e/aabb76791b6523a1b2d9dcbd"

    requestUrlCreator = RequestUrlCreator(url)
    onshapeAPI = OnshapeAPI(keys, requestUrlCreator)

    unitsList = [Units.METER,
                 Units.RADIAN,
                 Units.METER,
                 Units.METER]

    # numpyParameters = np.array([
    #                                     0.05, # Stroke Length
    #                                     0.18525, # Mounting Angle
    #                                     0.02,# Bore Diameter
    #                                     0.001]) # Original
    # numpyParameters = np.array([0.0358, 0.2446, 0.0289, 0.0000]) # A
    # numpyParameters = np.array([0.038880095, 0.0, 0.028061992, 0.060228433])  # B
    numpyParameters = np.array([0.038880095, 0.3, 0.028061992, 0.060228433])

    parameters = KinematicSampleConfigurationEncoder(unitsList=unitsList, numpyParameters=numpyParameters)
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
        SpineNames.MaxWidthCost: -0.2,
        SpineNames.MaxHeightCost: -0.2,
        SpineNames.MaxForceCost: 0.0,
        SpineNames.BoreDiameterCost: 0.0
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
    plt.show()





# print(json.dumps(costs.objectiveCosts, indent=4))

