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

access = 'I6M5WhNnlnrPeGGFucyKwlwa'
secret = 'W9qbMjKaYzfBRbg8MPoAuP7sDICkLhlByVYLAT8cehiF4Gbv'
keys = Keys(access, secret)
url = "https://cad.onshape.com/documents/6b351a18863dce94af4a4571/w/024504447ddcbbc5882aae07/e/3040b95620727a4e88cf17dd"

requestUrlCreator = RequestUrlCreator(url)
onshapeAPI = OnshapeAPI(keys, requestUrlCreator)

configurationEncoder = KinematicSampleConfigurationEncoder()
configurationEncoder.addParameter(ValueWithUnit(0.00, Units.METER))
configurationEncoder.addParameter(ValueWithUnit(-0.020, Units.METER))
configurationEncoder.addParameter(ValueWithUnit(0.00, Units.METER))
configurationEncoder.addParameter(ValueWithUnit(0.00, Units.METER))
configurationEncoder.addParameter(ValueWithUnit(0.00, Units.METER))
configurationEncoder.addParameter(ValueWithUnit(0.00, Units.METER))

tic = time.perf_counter()
parsed = onshapeAPI.doAPIRequestForJson(configurationEncoder, Names.SAMPLES_ATTRIBUTE_NAME)
toc = time.perf_counter()
print("time total " + str(toc - tic))

conversion = JsonToPython.toPythonStructure(parsed)

print(json.dumps(conversion, indent=2))

# value = conversion["Position"]["Jacobian"]
# print(value)


# print(json.dumps(parsed, indent=2))
