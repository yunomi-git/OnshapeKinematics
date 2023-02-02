# Class creates the payload to send via the Featurescript API endpoint

import onshapeComm.Names as names
class FeaturescriptCreator:
    def getAttribute(attributeName : str):
        script = """
        function (context is Context, queries is map)
        {{
            var instantiatedBodies = qHasAttribute(qEverything(EntityType.BODY), "{attributeName}");

            // This is what we are looking for
            var outputKinematics = getAttribute(context, {{"entity" : instantiatedBodies, "name" : "{attributeName}"}});
            return outputKinematics;
        }}
        """.format(attributeName = attributeName)
        queries = []
        return script, queries
    # def getOutputKinematics(self):
    #     return self.getAttribute(names.KINEMATICS_ATTRIBUTE_NAME)
    #
    # def getKinematicSamples(self):
    #     return self.getAttribute(names.SAMPLES_ATTRIBUTE_NAME)