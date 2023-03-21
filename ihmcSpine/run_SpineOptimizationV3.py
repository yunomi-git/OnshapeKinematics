import json
import matplotlib.pyplot as plt

import torch
import numpy as np
from onshapeInterface.OnshapeAPI import OnshapeAPI
from onshapeInterface.ConfigurationEncoder import KinematicSampleConfigurationEncoder, ValueWithUnit, Units
import onshapeInterface.Names as Names

from onshapeInterface.ConfigurationEncoder import ValueWithUnit, Units
from onshapeInterface.Keys import Keys
from onshapeInterface.RequestUrlCreator import RequestUrlCreator

from ihmcSpine.SpineCostEvaluator import SpineCostEvaluator, getBoreDiameter
from optimization.BayesOptWrapper import BayesOptOnshapeWrapper
import ihmcSpine.SpineNames as SpineNames
from optimization.ParameterBounds import ParameterBounds
from ihmcSpine.SpineVisualization import plotTorques

from data.DataFromCsv import DataFromCsv
from data.Data import Data
from data.VisualizeData import visualizeData


access = 'I6M5WhNnlnrPeGGFucyKwlwa'
secret = 'W9qbMjKaYzfBRbg8MPoAuP7sDICkLhlByVYLAT8cehiF4Gbv'
keys = Keys(access, secret)
url = "https://cad.onshape.com/documents/07c87d36d9881deeeea3d0c5/w/a5fc87e91bbbedea94bb5b58/e/aabb76791b6523a1b2d9dcbd"

requestUrlCreator = RequestUrlCreator(url)
onshapeAPI = OnshapeAPI(keys, requestUrlCreator)

minTorqueConstraint = 150.0
actuatorExtraLength = 0.063

# Negative means minimize
weights = {
    SpineNames.MaxWidthCost: -0.2,
    SpineNames.MaxHeightCost: -0.2,
    SpineNames.MaxForceCost: -0.05,
    SpineNames.BoreDiameterCost: 0.0
}

normalization = {
    SpineNames.MaxWidthCost: 0.05,
    SpineNames.MaxHeightCost: 0.14,
    SpineNames.MaxForceCost: 6000.0,
    SpineNames.BoreDiameterCost: 0.02
}
spineCostEvaluator = SpineCostEvaluator(weights=weights,
                                        normalization=normalization,
                                        minTorqueConstraint=minTorqueConstraint,
                                        actuatorExtraLength=actuatorExtraLength)

saveName = "ihmcSpine_V3Parameters"

if __name__ == "__main__":
    unitsList = [Units.METER,
                 Units.RADIAN,
                 Units.METER,
                 Units.METER]
    onshapeCostEvaluator = spineCostEvaluator.calculateCostFromOnshape
    bayesOptKinematicWrapper = BayesOptOnshapeWrapper(onshapeCostEvaluator=onshapeCostEvaluator,
                                                      onshapeAPI=onshapeAPI,
                                                      parameterDimensions=len(unitsList),
                                                      unitsList=unitsList)

    parameterBounds = ParameterBounds()
    parameterBounds.addBound(0.010, 0.300)              # Stroke Length
    parameterBounds.addBound(0.0, 1.57079633)           # Mounting Angle
    parameterBounds.addBound(0.00, 0.100)  # Extra Length Actuator
    parameterBounds.addBound(0.010, 0.030)              # Bore Diameter


    # Load old data
    dataExporter = DataFromCsv(saveName)
    data = dataExporter.loadData()


    initialParameter = KinematicSampleConfigurationEncoder(unitsList=unitsList)
    initialParameter.addParameters(np.array([0.05,  # Stroke Length
                                            0.18525,  # Mounting Angle
                                            0.001, # Extra Actuator
                                            0.02  # Bore Diameter
                                            ]))

    bestParam, bestCost = bayesOptKinematicWrapper.optimize(initialSamples=[initialParameter],
                                                            numIterations=40,
                                                            bounds=parameterBounds,
                                                            existingData=data)
    # Save data
    dataExporter.saveData(bayesOptKinematicWrapper.data)

    # Diagnostics
    print("===== Best Parameters")
    print("=========================")
    print(bestParam)
    bestParamToEncoding = KinematicSampleConfigurationEncoder(unitsList=unitsList, numpyParameters=bestParam.numpy())
    apiResponse = onshapeAPI.doAPIRequestForJson(bestParamToEncoding, Names.SAMPLES_ATTRIBUTE_NAME)
    costs = spineCostEvaluator.getMultiObjectiveCostFromOnshape(parameters=bestParam.numpy(), apiResponse=apiResponse)
    costs.print()
    boreDiameter = getBoreDiameter(bestParam.numpy())
    plotTorques(apiResponse, boreDiameter)
    print("")
    print("===== Original Parameters")
    print("=========================")
    apiResponse = onshapeAPI.doAPIRequestForJson(initialParameter, Names.SAMPLES_ATTRIBUTE_NAME)
    costs = spineCostEvaluator.getMultiObjectiveCostFromOnshape(parameters=initialParameter.numpyParameters, apiResponse=apiResponse)
    costs.print()
    print("")

    visualizeData(bayesOptKinematicWrapper.data)
    plt.show()



