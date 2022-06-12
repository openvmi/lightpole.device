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

        self._power = None #功率
        self._brightness = None  #亮度
        self._status = "normal" #路灯状态
        self._workMode = "smart" #工作模式: 智能模式

        self._employeeID = None
        self._employeeName = None
        self._employeeTemperature = None 

        self._deviceId =deviceId
        self._deviceArea = deviceArea

        self._weatherStationStatus = 'unknown'
        self._streetLightingStatus = 'unknown'
        self._inspectionStatus = 'unknown'
        self._emergencyPowerStatus = 'unknown'    

    def setWeatherStationStatus(self, status):
        self._weatherStationStatus = status
    
    def setStreetLightingStatus(self, status):
        self._streetLightingStatus = status

    def setInspectionStatus(self, status):
        self._inspectionStatus = status

    def setAdvertisingStatus(self, status):
        self._advertisingStatus = status
    
    def setEmergencyPowerStatus(self, status):
        self._emergencyPowerStatus = status

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

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        self._power = value

    @property
    def workMode(self):
        return self._workMode
    
    @workMode.setter
    def workMode(self, value):
        self._workMode = value

    @property
    def lightingLevel(self):
        return self._brightness
    
    @lightingLevel.setter
    def lightingLevel(self, value):
        self._brightness = value
    
    @property
    def lightingStatus(self):
        return self._status
    
    @lightingStatus.setter
    def lightingStatus(self, value):
        self._status = value

    @property
    def employeeID(self):
        return self._employeeID
    
    @employeeID.setter
    def employeeID(self, value):
        self._employeeID = value

    @property
    def employeeName(self):
        return self._employeeName

    @employeeName.setter
    def employeeName(self, value):
        self._employeeName = value
    
    @property
    def employeeTemperature(self):
        return self._employeeTemperature
    
    @employeeTemperature.setter
    def employeeTemperature(self, value):
        self._employeeTemperature = value

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
                "emergencyPowerSys": self._emergencyPowerStatus
            }
        }
        return ret
    
    def getSensorStatusInJson(self):
        ret = {
            "jsonrpc": "2.0",
            "method": "mqtt.notifySensorStatus",
            "params": {
                "deviceId": self._deviceId,
                "deviceArea": self._deviceArea
            }
        }
        weatherData = []
        weatherData.append(self._temperature)
        weatherData.append(self._humidity)
        weatherData.append(self._illuminance)
        weatherData.append(self._noise)
        weatherData.append(self._windSpeed)
        weatherData.append(self._rain)
        weatherData.append(self._pm2_5)
        weatherData.append(self._pm10)
        weatherData.append(self._carbonDioxide)
        ret["params"]["weatherStationSystem"] = weatherData
        streetLighting = {}
        streetLighting["power"] = self._power
        streetLighting["workMode"] = self._workMode
        streetLighting["lightingLevel"] = self._brightness
        streetLighting["status"] = self._status
        ret["params"]["streetLightingSystem"] = streetLighting
        return ret
    
    def getInspectionStatusInJson(self):
        ret = {
            "jsonrpc": "2.0",
            "method": "mqtt.notifyInspectionStatus",
            "params": {
                "deviceId": self._deviceId,
                "deviceArea": self._deviceArea
            }
        }
        inspectionData = {
            "employeeID": self._employeeID,
            "employeeName": self._employeeName,
            "employeeTemperature": self._employeeTemperature
        }
        ret["params"]["inspectionSystem"] = inspectionData
        return ret