from onshapeComm.ConfigurationEncoder import KinematicSampleConfigurationEncoder
from onshapeComm.ConfigurationEncoder import ValueWithUnit
from enum import Enum
import SpineNames
from onshapeComm import Names
import numpy as np
import math
import optimization.Costs as Costs

INVALID_COST = -1000


class SpineCostEvaluator:
    def __init__(self,
                 weights : dict,
                 normalization : dict,
                 minTorqueConstraint : float,
                actuatorExtraLength = 0.063, # Load cell and other stuff
                ):
        self.weights = weights
        self.normalization = normalization
        self.minTorqueConstraint = minTorqueConstraint
        self.actuatorLengthExtra = actuatorExtraLength

    # apiResponse the response from calling onshapeAPI.doAPIRequestForJson()
    def calculateCostFromOnshape(self, parameters : np.ndarray, apiResponse) -> float:
        multiObjCost =  getSpineCostsNd(apiResponse,
                                        parameters=parameters,
                                        minTorqueConstraint=self.minTorqueConstraint,
                                        actuatorExtraLength=self.actuatorLengthExtra,
                                        boreDiameterOverride=True,
                                        debug=False)
        if multiObjCost.constraintsMet:
            cost = 0
            costValues = multiObjCost.objectiveCosts
            for costName in costValues.keys():
                cost += costValues[costName] / self.normalization[costName] * self.weights[costName]
            return cost
        else:
            return INVALID_COST # Invalid cost



def getSpineCostsNd(apiResponse,
                    parameters : np.ndarray,
                    minTorqueConstraint : float,
                    actuatorExtraLength = 0.063, # Load cell and other stuff
                    boreDiameterOverride = False,
                    debug=False):
    # Constraints
    # Check validity at min ROM (Actuator length + min stroke) #
    # Check validity at max ROM (Actuator length + max stroke) #
    # max - min stroke <= 100
    # Look at sample of torques across ROM. Must be min xxx Nm. Function of bore diameter #

    # Optimize
    # Look at max width from crank #
    # Look at width of mounting point #
    # Look at max height of crank from mounting mount #
    # Look at bore diameter
    # Look at peak force from ^ sample of torques

    boreDiameter = 0.020
    if boreDiameterOverride:
        boreDiameter = getBoreDiameter(parameters)

    # Force and torques
    torques = getTorques(apiResponse, boreDiameter)
    minTorque = min(torques)
    minForces = forcesToReachMinTorque(apiResponse, minTorqueConstraint)
    maxForce = max(minForces)

    # Stroke
    minLength = getMinActuatorLength(apiResponse)
    maxLength = getMaxActuatorLength(apiResponse)
    strokeLength = maxLength - minLength

    # Size
    maxWidth = max([getMaxCrankWidth(apiResponse), getMountingWidth(apiResponse)])
    maxHeight = getMaxCrankHeight(apiResponse)

    # Constraints
    constraintsAreMet = True
    constraintsViolated = []
    if minTorque < minTorqueConstraint:
        constraintsAreMet = False
        constraintsViolated.append("Min Torque is too low")

    if strokeLength > 0.100:
        constraintsAreMet = False
        constraintsViolated.append("Stroke length > 0.1")

    if minLength < (actuatorExtraLength + strokeLength):
        constraintsViolated.append("Stroke does not fit in actuator")

    # Objective Calculation
    objectives = {SpineNames.MaxWidthCost : maxWidth,
                  SpineNames.MaxHeightCost : maxHeight,
                  SpineNames.MaxForceCost : maxForce,
                  SpineNames.BoreDiameterCost : boreDiameter}

    if debug:
        print("--- Diagnostics ---")
        print("Sample torques on ROM with bore diameter " + str(boreDiameter) + " m")
        print(torques)
        print("Sample forces to reach " + str(minTorqueConstraint) + " Nm on ROM:")
        print(minForces)

        print("Max Crank Width: " + str(getMaxCrankWidth(apiResponse)))
        print("Mounting Width: " + str(getMountingWidth(apiResponse)))
        print("Max Crank Height: " + str(getMaxCrankHeight(apiResponse)))

        print("Min Actuator Length: " + str(minLength))
        print("Max Actuator Length: " + str(maxLength))

        print("--- Evaluation ---")
        print("Min torque is: " + str(minTorque))
        print("Max force is: " + str(maxForce))
        print("Max Width = " + str(maxWidth))
        print("Max Height: " + str(maxHeight))


        print("Actuator Stroke Length: " + str(strokeLength))
        print("Bore Diameter: " + str(boreDiameter))

    if constraintsAreMet:
        return Costs.createMultiObjCost(objectives)
    else:
        return Costs.createInvalidMultiObjCost(constraintsViolated)

def getBoreDiameter(parameters : np.ndarray):
    return parameters[4]
def getTorques(apiResponse, boreDiameter):
    cylinderArea = math.pi * (boreDiameter/2.0) * (boreDiameter/2.0)
    jacobians = []
    for sample in apiResponse[SpineNames.SampleAllValues]["Range Output"]:
        jacobians.append(sample["Jacobian"])
    torquesToReturn = []
    for jacobianArr in jacobians:
        jacobian = np.array(jacobianArr)
        forces = np.array([2.0684e7 * cylinderArea])
        torques = np.dot(jacobian.T, forces)
        outputTorque = torques[0]
        torquesToReturn.append(outputTorque)
    return torquesToReturn

def forcesToReachMinTorque(apiResponse, desiredTorque):
    jacobians = []
    for sample in apiResponse[SpineNames.SampleAllValues]["Range Output"]:
        jacobians.append(sample["Jacobian"][0][0])
    minimumForces = []
    for jacobian in jacobians:
        force = desiredTorque / jacobian
        minimumForces.append(force)
    return minimumForces

def getMaxCrankWidth(apiResponse):
    return apiResponse[SpineNames.MaxCrankWidth][Names.KinematicAuxMeasurementInfo][SpineNames.CrankWidth]
def getMaxCrankHeight(apiResponse):
    return apiResponse[SpineNames.MaxCrankHeight][Names.KinematicAuxMeasurementInfo][SpineNames.CrankHeight]
def getMountingWidth(apiResponse):
    return apiResponse[SpineNames.MaxCrankWidth][Names.KinematicAuxMeasurementInfo][SpineNames.MountingWidth]

def getMinActuatorLength(apiResponse):
    return apiResponse[SpineNames.MinROM][Names.KINEMATICS_ATTRIBUTE_NAME][0]
def getMaxActuatorLength(apiResponse):
    return apiResponse[SpineNames.MaxROM][Names.KINEMATICS_ATTRIBUTE_NAME][0]

def isMinActuatorLengthMet(apiResponse):
    return apiResponse[SpineNames.MinROM][Names.KinematicAuxConstraintInfo][Names.ConstraintsOverallMet]