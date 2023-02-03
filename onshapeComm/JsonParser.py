from enum import Enum
from onshapeComm.ConfigurationEncoder import Units, ValueWithUnit

class OnshapeType(Enum):
    BTFSValueMap = 2062
    BTFSValueMapEntry = 2077
    BTFSValueString = 1422
    BTFSValueWithUnits = 1817
    BTFSValueArray = 1499
    BTFSValueBoolean = 1195
    BTFSValueNumber = 772


class JsonToPython:
    def toPythonStructure(message):
        return JsonToPython.parseMap(message["result"])

    def getType(value) -> OnshapeType:
        return value["type"]

    def parseUnknown(value):
        type = JsonToPython.getType(value)
        if (type == OnshapeType.BTFSValueMap.value):
            return JsonToPython.parseMap(value)
        elif (type == OnshapeType.BTFSValueArray.value):
            return JsonToPython.parseArray(value)
        elif (type == OnshapeType.BTFSValueWithUnits.value):
            return JsonToPython.parseValueWithUnitsInSI(value)
        elif (type == OnshapeType.BTFSValueString.value):
            return JsonToPython.parseString(value)
        elif (type == OnshapeType.BTFSValueBoolean.value):
            return JsonToPython.parseBoolean(value)
        elif (type == OnshapeType.BTFSValueNumber.value):
            return JsonToPython.parseNumber(value)
        else:
            print("JsonParser: unknown type parsed")
            print(type)

    def parseString(value) -> str:
        return value["message"]["value"]

    def parseArray(value):
        array = []
        numEl = len(value["message"]["value"])
        for i in range(numEl):
            parsed = JsonToPython.parseUnknown(value["message"]["value"][i])
            array.append(parsed)

        return array

    def parseMap(value):
        map = {}
        mapListJson = value["message"]["value"]
        numEl = len(mapListJson)
        for i in range(numEl):
            JsonToPython.parseMapEntryToMap(mapListJson[i], map)

        return map

    def parseMapEntryToMap(value, map):
        keyName = JsonToPython.parseString(value["message"]["key"])
        value = JsonToPython.parseUnknown(value["message"]["value"])

        map[keyName] = value

    def parseValueWithUnits(value) -> ValueWithUnit:
        numericValue = value["message"]["value"]
        unitsListJson = value["message"]["unitToPower"]

        # TODO: for now, only looking at 1d units. encode for multiD units
        unitName = unitsListJson[0]["key"]
        if unitName == "METER":
            unit = Units.METER
        elif unitName == "RADIAN":
            unit = Units.RADIAN

        return ValueWithUnit(numericValue, unit)

    def parseValueWithUnitsInSI(value):
        valueSI = value["message"]["value"]

        return valueSI

    def parseBoolean(value):
        return value["message"]["value"]

    def parseNumber(value):
        return value["message"]["value"]

