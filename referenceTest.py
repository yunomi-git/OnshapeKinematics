import torch
import numpy as np
from onshapeInterface.ConfigurationEncoder import KinematicSampleConfigurationEncoder, ValueWithUnit, Units

# class Caller:
#     def foo(self, input):
#         print(input)
#
# class Wrapper:
#     def __init__(self, thingToCall):
#         self.thingToCall = thingToCall
#
#     def doIt(self):
#         self.thingToCall("hello")
#
# caller = Caller()
# wrapper = Wrapper(caller.foo)
# wrapper.doIt()
#
# a = """hello: {name}""".format(name="a")
# print(a)

# a = torch.tensor(1).double()
# print(a.dtype)
# print(a.numpy()[0])

def appendXToList(xList, newX : np.ndarray):
    tensorX = torch.reshape(torch.from_numpy(newX).double(), (1, newX.size))
    if torch.numel(xList) == 0:
        return tensorX

    costList = torch.cat((xList, tensorX), dim=0)
    return costList


train_X = torch.tensor([[]])

initialParameter = KinematicSampleConfigurationEncoder()
initialParameter.addParameter(ValueWithUnit(0.10, Units.RADIAN)) # Crank Angle
initialParameter.addParameter(ValueWithUnit(0.0550, Units.METER)) # Crank Length
initialParameter.addParameter(ValueWithUnit(0.30, Units.RADIAN)) # Mounting Angle
initialParameter.addParameter(ValueWithUnit(0.10, Units.METER)) # Mounting Length
initialParameter.addParameter(ValueWithUnit(0.02, Units.METER)) # Bore Diameter

# train_X = ((2 * torch.rand(initialPoints, self.parameterDimensions) - 1.0) * 5).double()  # in meters

train_X = appendXToList(train_X, initialParameter.numpyParameters)
train_X = appendXToList(train_X, initialParameter.numpyParameters)
print(train_X)