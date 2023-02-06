import numpy as np
import json
import onshapeComm.Names as Names
from ihmcAnkle.AnkleConfiguration import AnkleConfiguration
import numpy as Numpy
import mathUtil.UnitConversions as uc

INVALID_COST = -1000000.0

class AnkleSamples:
    sample0_0 = "sample0_0"
    sample0_25 = "sample0_25"
    rom0Roll = "rom0Roll"
    rom25Roll = "rom25Roll"
    sampleMaxPitch_25 = "sampleMaxPitch_25"
    maxForwardSweptPitch = "maxForwardSweptPitch"
    sampleMaxForwardSwept = "sampleMaxForwardSwept"
    sampleMinPitch_0 = "sampleMinPitch_0"
    sampleTorquePitch_0 = "sampleTorquePitch_0"

class AnkleDefinition:
    InnerMaxLength = "InnerMaxLength"
    InnerMinLength = "InnerMinLength"
    OuterMaxLength = "OuterMaxLength"
    OuterMinLength = "OuterMinLength"

    InnerForwardSweptAngle = "InnerForwardSweptAngle"
    OuterForwardSweptAngle = "OuterForwardSweptAngle"

class AnkleCosts:
    def __init__(self, sideSweep, forwardSweep, pitchForwardMaxRoll, pitchForward0Roll, torque):
        self.sideSweep = sideSweep
        self.forwardSweep = forwardSweep
        self.pitchForwardMaxRoll = pitchForwardMaxRoll
        self.pitchForward0ROll = pitchForward0Roll
        self.torque = torque
        self.invalidParameters = False

    def createInvalidCost():
        cost = AnkleCosts(0,0,0,0,0)
        cost.setInvalidParameters()
        return cost

    def setInvalidParameters(self):
        self.invalidParameters = True

    def parametersAreInvalid(self):
        return self.invalidParameters

    def print(self):
        if not self.invalidParameters:
            print("Costs:")
            print(json.dumps({
                "sideSweep" : str(self.sideSweep * uc.M_TO_MM) + " mm",
                "forwardSweep" : str(self.forwardSweep * uc.RAD_TO_DEG) + " deg",
                "pitchForwardMaxRoll" : str(self.pitchForwardMaxRoll * uc.RAD_TO_DEG) + " deg",
                "pitchForward0Roll" : str(self.pitchForward0ROll * uc.RAD_TO_DEG) + " deg",
                "torque" : str(self.torque) + " Nm"
            }, indent=4))

        else:
            print("Invalid Parameters")

class AnkleCostEvaluator:
    def __init__(self):
        pass

    # apiResponse the response from calling onshapeAPI.doAPIRequestForJson()
    def calculateCostFromOnshape(parameters : AnkleConfiguration, apiResponse) -> AnkleCosts:
        # Collision check at 0,0
        collision0_0avoided = apiResponse[AnkleSamples.sample0_0][Names.KinematicAuxConstraintInfo][Names.ConstraintsOverallMet]
        collision0_25avoided = apiResponse[AnkleSamples.sample0_25][Names.KinematicAuxConstraintInfo][Names.ConstraintsOverallMet]
        if ((not collision0_0avoided) or (not collision0_25avoided)):
            return AnkleCosts.createInvalidCost()
        maxPitch0r = apiResponse[AnkleSamples.rom0Roll]
        maxPitch25r = apiResponse[AnkleSamples.rom25Roll]

        if not AnkleSamples.sampleMaxPitch_25 in apiResponse:
            return AnkleCosts.createInvalidCost()
        collisionMaxPitch_25Avoided = apiResponse[AnkleSamples.sampleMaxPitch_25][Names.KinematicAuxConstraintInfo][Names.ConstraintsOverallMet]
        if not collisionMaxPitch_25Avoided:
            return AnkleCosts.createInvalidCost()

        # maxForwardSweptPitch = apiResponse[AnkleSamples.maxForwardSwept]
        maxForwardSweptAngle = apiResponse[AnkleSamples.sampleMaxForwardSwept][Names.KinematicAuxMeasurementInfo][AnkleDefinition.InnerForwardSweptAngle]

        rom30ActuatorLengthsValid = apiResponse[AnkleSamples.sampleMinPitch_0][Names.KinematicAuxConstraintInfo][Names.ConstraintsOverallMet]
        if not rom30ActuatorLengthsValid:
            return AnkleCosts.createInvalidCost()

        minForwardSweptAngleCand1 = apiResponse[AnkleSamples.sampleMaxPitch_25][Names.KinematicAuxMeasurementInfo][AnkleDefinition.InnerForwardSweptAngle]
        minForwardSweptAngleCand2 = apiResponse[AnkleSamples.sampleMinPitch_0][Names.KinematicAuxMeasurementInfo][AnkleDefinition.InnerForwardSweptAngle]
        minForwardSweptAngle = min(minForwardSweptAngleCand1, minForwardSweptAngleCand2)
        forwardSweep = maxForwardSweptAngle - minForwardSweptAngle

        sideSweep = parameters.relativeY.value + parameters.globalY.value

        jacobianArray = apiResponse[AnkleSamples.sampleTorquePitch_0][Names.JacobianSample]
        jacobian = np.array(jacobianArray)
        forces = np.array([7500, 7500])
        torques = np.dot(jacobian.T, forces)
        pitchTorque = torques[0]

        return AnkleCosts(sideSweep=sideSweep,
                          forwardSweep=forwardSweep,
                          pitchForward0Roll=maxPitch0r,
                          pitchForwardMaxRoll=maxPitch25r,
                          torque=pitchTorque)




