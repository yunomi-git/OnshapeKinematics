import requests
import json 
from onshapeComm.RequestUrlCreator import RequestUrlCreator
from onshape_client.client import Client
from onshape_client.onshape_url import OnshapeElement
import time
from onshapeComm.FeaturescriptPayloadCreator import FeaturescriptCreator
import onshapeComm.Names as Names


class ValueWithUnit:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

class ConfigurationEncodingCreator:
    # [Configuration(name, value, unit), ...]
    def getConfigurationEncoding(configurationList):
        encoding = ""
        i = 1
        for config in configurationList:
            encoding +=  "Input" + str(i) + "="
            encoding += str(config.value) + " "
            encoding += config.unit + ";"
            i += 1
        if len(configurationList) == 1:
            encoding = encoding[:-1]
        return encoding

class OnshapeKinematicsAPI:
    def __init__(self, accessKey, secretKey, url, numInputs):
        base = 'https://cad.onshape.com'
        self.client = Client(configuration={"base_url": base,
                                    "access_key": accessKey,
                                    "secret_key": secretKey})
        self.urlCreator = RequestUrlCreator(url)

        self.headers = {'Accept': 'application/vnd.onshape.v1+json; charset=UTF-8;qs=0.1',
                'Content-Type': 'application/json'}
        self.numInputs = numInputs
    
    # inputs is np array, unitsList is string array
    def getOutputKinematics(self, inputs, unitsList):
        # Setup the request
        script, queries = FeaturescriptCreator.getAttribute(Names.KINEMATICS_ATTRIBUTE_NAME)
        self.urlCreator.setRequest("featurescript")
        api_url = self.urlCreator.getURL()

        inputsAsVWU = []
        for i in range(self.numInputs):
            inputsAsVWU.append(ValueWithUnit(inputs[i], unitsList[i]))
        config = ConfigurationEncodingCreator.getConfigurationEncoding(inputsAsVWU)

        params = {'configuration' : config}

        payload = {
            "script": script,
            "queries" : queries,
            }

        # Send the request to onshape
        response = self.client.api_client.request(method = 'POST', 
                                        url=api_url, 
                                        query_params=params, 
                                        headers=self.headers, 
                                        body=payload)
        parsed = json.loads(response.data)

        # Interpret json response as python data structure
        numData = len(parsed["result"]["message"]["value"])
        output = []
        # unit = parsed["result"]["message"]["value"][0]["message"]["unitToPower"]
        for i in range(numData):
            value = parsed["result"]["message"]["value"][i]["message"]["value"]
            output.append(value)
        
        return output




