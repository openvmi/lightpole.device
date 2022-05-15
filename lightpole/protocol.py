from os import stat
import re


class Protocol:
    def __init__(self, deviceId, deviceArea) -> None:
        self._speedWind = None
        self._deviceId =deviceId
        self._deviceArea = deviceArea
        self._weatherStationStatus = 'unknown'
        self._streetLightingStatus = 'unknown'
        self._inspectionStatus = 'unknown'
        self._advertisingStatus = 'unknown'

    def setWeatherStationStatus(self, status):
        self._weatherStationStatus = status
    
    def setStreetLightingStatus(self, status):
        self._streetLightingStatus = status

    def setInspectionStatus(self, status):
        self._inspectionStatus = status

    def setAdvertisingStatus(self, status):
        self._advertisingStatus = status

    def getPingInJson(self):
        ret = {
            "jsonrpc": "2.0",
            "method": "mqtt.ping",
            "params": {
                "deviceId": self._deviceId,
                "deviceArea": self._deviceArea,
                "weatherStationSys": self._weatherStationStatus,
                "streetLightingSys": self._streetLightingStatus,
                "inspectionSys": self._inspectionStatus,
                "advertisingSys": self._advertisingStatus
            }
        }
        return ret
    
    def getDataInJson(self):
        ret = {
            "jsonrpc": "2.0",
            "method": "mqtt.notifySensorStatus",
            "params": {
                "deviceId": self._deviceId,
                "deviceArea": self._deviceArea
            }
        }
        return ret