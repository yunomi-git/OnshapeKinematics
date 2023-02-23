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
from ihmcAnkle.AnkleConfiguration import AnkleConfiguration
from ihmcAnkle.AnkleCost import AnkleCostEvaluator, AnkleCosts

access = 'I6M5WhNnlnrPeGGFucyKwlwa'
secret = 'W9qbMjKaYzfBRbg8MPoAuP7sDICkLhlByVYLAT8cehiF4Gbv'
keys = Keys(access, secret)
url = "https://cad.onshape.com/documents/6b351a18863dce94af4a4571/w/024504447ddcbbc5882aae07/e/3040b95620727a4e88cf17dd"

requestUrlCreator = RequestUrlCreator(url)
onshapeAPI = OnshapeAPI(keys, requestUrlCreator)

parameters = AnkleConfiguration()
parameters.setNewConfiguration(globalX=ValueWithUnit(0.00, Units.METER),
                                 globalY=ValueWithUnit(0.0, Units.METER),
                                 globalZ=ValueWithUnit(0.00, Units.METER),
                                 relativeX=ValueWithUnit(0.00, Units.METER),
                                 relativeY=ValueWithUnit(0.00, Units.METER),
                                 relativeZ=ValueWithUnit(0.00, Units.METER))

# tic = time.perf_counter()
apiResponse = onshapeAPI.doAPIRequestForJson(parameters, Names.SAMPLES_ATTRIBUTE_NAME)
# toc = time.perf_counter()

print(json.dumps(apiResponse, indent=4))
# print("time total " + str(toc - tic))

costs = AnkleCostEvaluator.calculateCostFromOnshape(parameters, apiResponse)
costs.print()

# value = conversion["Position"]["Jacobian"]
# print(value)


# print(json.dumps(parsed, indent=2))
