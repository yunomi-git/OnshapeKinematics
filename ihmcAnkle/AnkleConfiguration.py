from onshapeComm.ConfigurationEncoder import KinematicSampleConfigurationEncoder
class AnkleConfiguration(KinematicSampleConfigurationEncoder):
    def __init__(self):
        super(AnkleConfiguration, self).__init__()

    def setNewConfiguration(self, globalX, globalY, globalZ, relativeX, relativeY, relativeZ):
        self.clearEncoding()
        self.addParameter(globalX)
        self.addParameter(globalY)
        self.addParameter(globalZ)
        self.addParameter(relativeX)
        self.addParameter(relativeY)
        self.addParameter(relativeZ)
