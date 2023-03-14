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
import math
import matplotlib.pyplot as plt
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