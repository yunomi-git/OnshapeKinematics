import requests
import json
from onshapeComm.RequestUrlCreator import RequestUrlCreator
from onshape_client.client import Client
from onshape_client.onshape_url import OnshapeElement
from onshapeComm.FeaturescriptPayloadCreator import FeaturescriptCreator
import time

from onshapeComm.ConfigurationEncoder import ConfigurationEncoder
from onshapeComm.Keys import Keys
from onshapeComm.RequestUrlCreator import RequestUrlCreator

class OnshapeAPI:
    def __init__(self, keys : Keys, requestUrlCreator : RequestUrlCreator):
        base = 'https://cad.onshape.com'
        self.client = Client(configuration={"base_url": base,
                                            "access_key": keys.getAccessKey(),
                                            "secret_key": keys.getSecretKey()})

        self.headers = {'Accept': 'application/vnd.onshape.v1+json; charset=UTF-8;qs=0.1',
                        'Content-Type': 'application/json'}

        # Set up featurescript to do the request
        requestUrlCreator.setRequest("featurescript")
        self.api_url = requestUrlCreator.getURL()


    # inputs is np array, unitsList is string array
    def doAPIRequestForJson(self, configuration : ConfigurationEncoder, attributeName : str):
        # Configuration of the request
        config = configuration.getEncoding()
        params = {'configuration': config}
        print(config)

        # Featurescript to extract attributes of request
        script, queries = FeaturescriptCreator.getAttribute(attributeName)
        payload = {
            "script": script,
            "queries": queries,
        }

        # Send the request to onshape
        response = self.client.api_client.request(method='POST',
                                                  url=self.api_url,
                                                  query_params=params,
                                                  headers=self.headers,
                                                  body=payload)
        parsed = json.loads(response.data)

        # # Interpret json response as python data structure
        # numData = len(parsed["result"]["message"]["value"])
        # output = []
        # # unit = parsed["result"]["message"]["value"][0]["message"]["unitToPower"]
        # for i in range(numData):
        #     value = parsed["result"]["message"]["value"][i]["message"]["value"]
        #     output.append(value)

        return parsed




