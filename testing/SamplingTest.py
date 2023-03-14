from onshapeInterface.OnshapeAPI import OnshapeAPI
from mathUtil.kinematics import KinematicsToolbox, Unit
import numpy as np
import time
import json
import matplotlib.pyplot as plt

from onshapeInterface.ConfigurationEncoder import KinematicSampleConfigurationEncoder, ValueWithUnit, Units
from onshapeInterface.Keys import Keys
from onshapeInterface.RequestUrlCreator import RequestUrlCreator
import onshapeInterface.Names as Names
from onshapeInterface.JsonParser import JsonToPython

access = 'Eiu0FEHRtfHMUd8e3dovW6wR'
secret = 'YmluDgPnCePqppY6xPnH2hOhtN6nhT3R4Mwus6Cc7CJQDFSk'
keys = Keys(access, secret)
url = "https://cad.onshape.com/documents/b9737280bc45ea1f3d8ee974/w/cde3b2b5d6720c142e2bbe87/e/957e5718dbad4220c7ffdc3d"

requestUrlCreator = RequestUrlCreator(url)
onshapeAPI = OnshapeAPI(keys, requestUrlCreator)

configurationEncoder = KinematicSampleConfigurationEncoder()
configurationEncoder.addParameter(ValueWithUnit(0.07, Units.METER))

tic = time.perf_counter()
apiResponse = onshapeAPI.doAPIRequestForJson(configurationEncoder, Names.SAMPLES_ATTRIBUTE_NAME)
toc = time.perf_counter()

# print(json.dumps(apiResponse, indent=2))
print("time total " + str(toc - tic))

range = apiResponse["Range"]
numel = len(range)
inputsAll = range[Names.SAMPLE_RANGE_INPUT_ATTR_NAME]
outputsAll = range[Names.SAMPLE_RANGE_OUTPUT_ATTR_NAME]
inputs = [x[0]for x in inputsAll]
outputs = [x[Names.KinematicAuxMeasurementInfo]["Hypotenuse"] for x in outputsAll]

plt.plot(inputs, outputs)
plt.show()

print(inputs)
print(outputs)
