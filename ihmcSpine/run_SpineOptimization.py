import json

import torch
import numpy as np
from onshapeInterface.OnshapeAPI import OnshapeAPI
from onshapeInterface.ConfigurationEncoder import KinematicSampleConfigurationEncoder, ValueWithUnit, Units
import onshapeInterface.Names as Names

from onshapeInterface.ConfigurationEncoder import ValueWithUnit, Units
from onshapeInterface.Keys import Keys
from onshapeInterface.RequestUrlCreator import RequestUrlCreator

from ihmcSpine.SpineCostEvaluator import SpineCostEvaluator
from optimization.BayesOptWrapper import BayesOptOnshapeWrapper
import ihmcSpine.SpineNames as SpineNames
from optimization.ParameterBounds import ParameterBounds

from data.DataFromCsv import DataFromCsv
from data.Data import Data

access = 'I6M5WhNnlnrPeGGFucyKwlwa'
secret = 'W9qbMjKaYzfBRbg8MPoAuP7sDICkLhlByVYLAT8cehiF4Gbv'
keys = Keys(access, secret)
url = "https://cad.onshape.com/documents/c6a60909a9693027fe5bb9e9/w/50fafe234fce490c861a55b4/e/917b3052222d7c5ffe909970"

requestUrlCreator = RequestUrlCreator(url)
onshapeAPI = OnshapeAPI(keys, requestUrlCreator)

minTorqueConstraint = 150.0
actuatorExtraLength = 0.063

# Negative means minimize
weights = {
    SpineNames.MaxWidthCost: -0.2,
    SpineNames.MaxHeightCost: -0.2,
    SpineNames.MaxForceCost: -0.3,
    SpineNames.BoreDiameterCost: -0.1
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

saveName = "ihmcAnkle"

if __name__ == "__main__":
    unitsList = [Units.RADIAN,
                 Units.METER,
                 Units.RADIAN,
                 Units.METER,
                 Units.METER]
    onshapeCostEvaluator = spineCostEvaluator.calculateCostFromOnshape
    bayesOptKinematicWrapper = BayesOptOnshapeWrapper(onshapeCostEvaluator=onshapeCostEvaluator,
                                                      onshapeAPI=onshapeAPI,
                                                      parameterDimensions=len(unitsList),
                                                      unitsList=unitsList)

    parameterBounds = ParameterBounds()
    parameterBounds.addBound(-1.57079633, 1.57079633)   # Crank Angle
    parameterBounds.addBound(0.010, 0.300)              # Crank Length
    parameterBounds.addBound(0.0, 1.57079633)           # Mounting Angle
    parameterBounds.addBound(0.010, 0.300)              # Mounting Length
    parameterBounds.addBound(0.010, 0.030)              # Bore Diameter

    # Load old data
    dataExporter = DataFromCsv(saveName)
    data = dataExporter.loadData()


    initialParameter = KinematicSampleConfigurationEncoder(unitsList=unitsList)
    initialParameter.addParameters(np.array([0.1745,  # Crank Angle
                                             0.060, # Crank Length
                                             0.611, # Mounting Angle
                                             0.200, # Mounting Length
                                             0.02])) # Bore Diameter

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
    print("")
    print("===== Original Parameters")
    print("=========================")
    apiResponse = onshapeAPI.doAPIRequestForJson(initialParameter, Names.SAMPLES_ATTRIBUTE_NAME)
    costs = spineCostEvaluator.getMultiObjectiveCostFromOnshape(parameters=initialParameter.numpyParameters, apiResponse=apiResponse)
    costs.print()
    print("")

