from onshapeComm.ConfigurationEncoder import KinematicSampleConfigurationEncoder
from onshapeComm.ConfigurationEncoder import ValueWithUnit
class AnkleConfiguration(KinematicSampleConfigurationEncoder):
    def __init__(self):
        super(AnkleConfiguration, self).__init__()

    def setNewConfiguration(self, globalX : ValueWithUnit,
                            globalY : ValueWithUnit,
                            globalZ : ValueWithUnit,
                            relativeX : ValueWithUnit,
                            relativeY : ValueWithUnit,
                            relativeZ : ValueWithUnit):
        self.clearEncoding()
        self.addParameter(globalX)
        self.addParameter(globalY)
        self.addParameter(globalZ)
        self.addParameter(relativeX)
        self.addParameter(relativeY)
        self.addParameter(relativeZ)

        self.globalX = globalX
        self.globalY = globalY
        self.globalZ = globalZ
        self.relativeX = relativeX
        self.relativeY = relativeY
        self.relativeZ = relativeZ
