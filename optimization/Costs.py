class MultiObjCost:
    def __init__(self):
        self.objectiveCosts = {}
        self.constraintsMet = True
        self.violatedConstraints = []

    def print(self):
        if self.constraintsMet:
            for objective in self.objectiveCosts.keys():
                print(objective + ": " + self.objectiveCosts[objective])
        else:
            print("Constraints have been violated: ")
            for constraint in self.violatedConstraints:
                print("\t" + constraint)

def createMultiObjCost(objectiveCosts : dict):
    costs = MultiObjCost()
    costs.objectiveCosts = objectiveCosts
    return costs

def createInvalidMultiObjCost(violatedConstraints : list):
    costs = MultiObjCost()
    costs.constraintsMet = False
    costs.violatedConstraints = violatedConstraints
    return costs
