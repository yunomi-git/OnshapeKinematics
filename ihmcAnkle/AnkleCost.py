
INVALID_COST = 1000000.0
class AnkleCostEvaluator:
    def __init__(self):
        pass

    # apiResponse the response from calling onshapeAPI.doAPIRequestForJson()
    def calculateCostFromOnshape(self, apiResponse):
        # Collision check at 0,0
        collision1 = apiResponse[collision0_0][KinematicAuxConstraintInfo][overallConstraintsMet]
        collision1 = apiResponse[collision0_25][KinematicAuxConstraintInfo][overallConstraintsMet]

        maxPitch = apiResponse[collision0_25][KinematicAuxConstraintInfo][overallConstraintsMet]
