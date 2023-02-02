from onshapeComm.OnshapeAPI import OnshapeAPI
from mathUtil.kinematics import KinematicsToolbox, Unit
import numpy as np
import time
import json

from onshapeComm.ConfigurationEncoder import KinematicSampleConfigurationEncoder, ValueWithUnit, Units
from onshapeComm.Keys import Keys
from onshapeComm.RequestUrlCreator import RequestUrlCreator
import onshapeComm.Names as Names
from onshapeComm.JsonParser import JsonToPython

access = 'Eiu0FEHRtfHMUd8e3dovW6wR'
secret = 'YmluDgPnCePqppY6xPnH2hOhtN6nhT3R4Mwus6Cc7CJQDFSk'
keys = Keys(access, secret)
url = "https://cad.onshape.com/documents/b9737280bc45ea1f3d8ee974/w/cde3b2b5d6720c142e2bbe87/e/957e5718dbad4220c7ffdc3d"

requestUrlCreator = RequestUrlCreator(url)

onshapeAPI = OnshapeAPI(keys, requestUrlCreator)

configurationEncoder = KinematicSampleConfigurationEncoder()
configurationEncoder.addParameter(ValueWithUnit(0.05, Units.METER))
parsed = onshapeAPI.doAPIRequestForJson(configurationEncoder, Names.SAMPLES_ATTRIBUTE_NAME)
conversion = JsonToPython.toPythonStructure(parsed)
# print(json.dumps(conversion, indent=2))

print(json.dumps(parsed, indent=2))
