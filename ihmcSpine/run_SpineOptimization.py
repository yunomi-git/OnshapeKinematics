import json

import torch
import numpy as np
from onshapeComm.OnshapeAPI import OnshapeAPI
from onshapeComm.ConfigurationEncoder import KinematicSampleConfigurationEncoder, ValueWithUnit, Units
import onshapeComm.Names as Names

from onshapeComm.ConfigurationEncoder import ValueWithUnit, Units
from onshapeComm.Keys import Keys
from onshapeComm.RequestUrlCreator import RequestUrlCreator

from ihmcSpine.SpineCostEvaluator import SpineCostEvaluator
from optimization.BayesOptWrapper import BayesOptOnshapeWrapper
import ihmcSpine.SpineNames as SpineNames
from optimization.ParameterBounds import ParameterBounds

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
    # TODO: also options to load past data, select specific points to sample
    parameterBounds = ParameterBounds()
    parameterBounds.addBound(-1.57079633, 1.57079633)   # Crank Angle
    parameterBounds.addBound(0.010, 0.300)              # Crank Length
    parameterBounds.addBound(0.0, 1.57079633)           # Mounting Angle
    parameterBounds.addBound(0.010, 0.300)              # Mounting Length
    parameterBounds.addBound(0.010, 0.030)              # Bore Diameter

    initialParameter = KinematicSampleConfigurationEncoder(unitsList=unitsList)
    initialParameter.addParameters(np.array([0.10,  # Crank Angle
                                             0.055, # Crank Length
                                             0.30, # Mounting Angle
                                             0.10, # Mounting Length
                                             0.20])) # Bore Diameter
    # initialParameter.addParameter(ValueWithUnit(0.10, Units.RADIAN)) # Crank Angle
    # initialParameter.addParameter(ValueWithUnit(0.0550, Units.METER)) # Crank Length
    # initialParameter.addParameter(ValueWithUnit(0.30, Units.RADIAN)) # Mounting Angle
    # initialParameter.addParameter(ValueWithUnit(0.10, Units.METER)) # Mounting Length
    # initialParameter.addParameter(ValueWithUnit(0.02, Units.METER)) # Bore Diameter

    bestParam, bestCost = bayesOptKinematicWrapper.optimize(initialSamples=[initialParameter],
                                                            numIterations=10,
                                                            bounds=parameterBounds)
    # TODO: also select where to save this run

    print("Best Parameters")
    print(bestParam)
    bestParamToEncoding = KinematicSampleConfigurationEncoder(unitsList=unitsList, numpyParameters=bestParam.numpy())
    apiResponse = onshapeAPI.doAPIRequestForJson(bestParamToEncoding, Names.SAMPLES_ATTRIBUTE_NAME)
    costs = SpineCostEvaluator.getSpineCostsNd(apiResponse,
                                               parameters=bestParamToEncoding.numpyParameters,
                                               minTorqueConstraint=minTorqueConstraint,
                                               actuatorExtraLength=actuatorExtraLength,
                                               boreDiameterOverride=True,
                                               debug=True)
    costs.print()
    bayesOptKinematicWrapper.evaluateCostWrapper(bestParam)
    print("Original Parameters")
    bayesOptKinematicWrapper.evaluateCostWrapper(torch.tensor([0,0,0,0,0]))

