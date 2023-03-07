import math
import matplotlib.pyplot as plt

from onshapeComm.OnshapeAPI import OnshapeAPI
from mathUtil.kinematics import KinematicsToolbox, Unit
import numpy as np
import time
import json
import ihmcSpine.SpineNames as SpineNames

from onshapeComm.ConfigurationEncoder import KinematicSampleConfigurationEncoder, ValueWithUnit, Units
from onshapeComm.Keys import Keys
from onshapeComm.RequestUrlCreator import RequestUrlCreator
import onshapeComm.Names as Names
from onshapeComm.JsonParser import JsonToPython
from ihmcSpine import SpineCostEvaluator


def plotTorques(apiResponse, boreDiameter):
    cylinderArea = math.pi * (boreDiameter/2.0) * (boreDiameter/2.0)
    jacobians = []
    for sample in apiResponse[SpineNames.SampleAllValues]["Range Output"]:
        jacobians.append(sample["Jacobian"])
    outputTorques = []
    for jacobianArr in jacobians:
        jacobian = np.array(jacobianArr)
        forces = np.array([2.0684e7 * cylinderArea])
        torques = np.dot(jacobian.T, forces)
        outputTorque = torques[0]
        outputTorques.append(outputTorque)

    angles = apiResponse[SpineNames.SampleAllValues]["Range Input"]

    fig, ax = plt.subplots()
    ax.scatter(angles, outputTorques)
    plt.xlabel("Spine Angle (rad)")
    plt.ylabel("Torques (Nm)")
    plt.show()

if __name__ == "__main__":
    access = 'I6M5WhNnlnrPeGGFucyKwlwa'
    secret = 'W9qbMjKaYzfBRbg8MPoAuP7sDICkLhlByVYLAT8cehiF4Gbv'
    keys = Keys(access, secret)
    url = "https://cad.onshape.com/documents/c6a60909a9693027fe5bb9e9/w/50fafe234fce490c861a55b4/e/917b3052222d7c5ffe909970"

    requestUrlCreator = RequestUrlCreator(url)
    onshapeAPI = OnshapeAPI(keys, requestUrlCreator)

    parameters = KinematicSampleConfigurationEncoder()
    parameters.addParameter(ValueWithUnit(0.00, Units.RADIAN))
    parameters.addParameter(ValueWithUnit(0.10, Units.METER))
    parameters.addParameter(ValueWithUnit(0.00, Units.RADIAN))
    parameters.addParameter(ValueWithUnit(0.20, Units.METER))
    parameters.addParameter(ValueWithUnit(0.02, Units.METER))

    tic = time.perf_counter()
    apiResponse = onshapeAPI.doAPIRequestForJson(parameters, Names.SAMPLES_ATTRIBUTE_NAME)
    toc = time.perf_counter()

    print(json.dumps(apiResponse, indent=4))
    print("time total " + str(toc - tic))

    costs = SpineCostEvaluator.getSpineCostsNd(apiResponse,
                                               parameters=parameters.numpyParameters,
                                               minTorqueConstraint=150.0,
                                               actuatorExtraLength=0.063,
                                               boreDiameterOverride=True,
                                               debug=True)
    costs.print()

    plotTorques(apiResponse, SpineCostEvaluator.getBoreDiameter(parameters.numpyParameters))




# print(json.dumps(costs.objectiveCosts, indent=4))

