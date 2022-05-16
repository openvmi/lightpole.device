from os import stat
import re


class Protocol:
    def __init__(self, deviceId, deviceArea) -> None:
        self._temperature = None #温度
        self._humidity = None #湿度
        self._illuminance = None  # 光照度
        self._noise = None #噪音
        self._windSpeed = None  #风速
        self._rain = None #雨量
        self._pm2_5 = None #pm2.5
        self._pm10 = None  #pm10
        self._carbonDioxide = None #二氧化碳

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

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter 
    def temperature(self, temperature):
        self._temperature = temperature

    @property
    def humidity(self):
        return self._humidity
        
    @humidity.setter
    def humidity(self, humidity):
        self._humidity = humidity
    
    @property
    def illuminance(self):
        return self._illuminance

    @illuminance.setter
    def illuminance(self, value):
        self._illuminance = value

    @property
    def noise(self):
        return self._noise

    @noise.setter
    def noise(self, value):
        self._noise = value

    @property
    def windsSpeed(self):
        return self._windSpeed
    
    @windsSpeed.setter
    def windsSpeed(self, value):
        self._windSpeed = value

    @property
    def rain(self):
        return self._rain

    @rain.setter
    def rain(self, value):
        self._rain = value

    @property
    def pm2_5(self):
        return self._pm2_5
    
    @pm2_5.setter
    def pm2_5(self, value):
        self._pm2_5 = value
    
    @property
    def pm10(self):
        return self._pm10
    
    @pm10.setter
    def pm10(self, value):
        self._pm10 = value
    
    @property
    def carbonDioxide(self):
        return self._carbonDioxide
    
    @carbonDioxide.setter
    def carbonDioxide(self, value):
        self._carbonDioxide = value

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