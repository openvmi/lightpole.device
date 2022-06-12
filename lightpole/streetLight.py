from unittest import result


class StreetLighting:
    def __init__(self, channel) -> None:
        self._channel = channel
        self._iccardStatus = 'unknown'
        self._inputvoltageStatus = 'unknown'
        self._outputcurrentStatus = 'unknown'
        self._outputpowerStatus = 'unknown'
        self._electricityConsumptionStatus = 'unknown'
        self._brightnessStatus = 'unknown'
        self._brightness = 0

        self._workMode = "smart"

    @property
    def iccard(self):
        command = bytes([0x04, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x5E])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._iccardStatus = 'error'
        else:
            self._iccardStatus = 'normal'
        return result

    @property
    def inputvoltage(self):
        command = bytes([0x05, 0x04, 0x00, 0x04, 0x00, 0x01, 0x71, 0x8F])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._inputvoltageStatus = 'error'
        else:
            self._inputvoltageStatus = 'normal'
        return result

    @property
    def outputcurrent(self):
        command = bytes([0x05, 0x04, 0x00, 0x05, 0x00, 0x01, 0x20, 0x4F])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._outputcurrentStatus = 'error'
        else:
            self._outputcurrentStatus = 'normal'
        return result

    @property
    def outputpower(self):
        command = bytes([0x05, 0x04, 0x00, 0x06, 0x00, 0x01, 0xD0, 0x4F])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._outputpowerStatus = 'error'
        else:
            self._outputpowerStatus = 'normal'
        return result

    @property
    def electricityConsumption(self):
        command = bytes([0x05, 0x04, 0x00, 0x08, 0x00, 0x01, 0xB1, 0x8C])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._electricityConsumptionStatus = 'error'
        else:
            self._electricityConsumptionStatus = 'normal'
        return result
   

    @property
    def brightness(self):
        command = bytes([0x05, 0x06, 0x00, 0x04, 0x00, 0x32, 0x48, 0x5A])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._brightnessStatus = 'error'
        else:
            self._brightnessStatus = 'normal'
        return result

    @brightness.setter
    def brightness(self, value):
        print('trying to set brightness')
        self._brightness = value
    
    def _checkStatus(self, status):
        if self._iccardStatus == status and \
            self._inputvoltageStatus == status and \
            self._outputcurrentStatus == status and \
            self._outputpowerStatus == status and \
            self._electricityConsumptionStatus == status and \
            self._brightnessStatus == status :
            return True
            
    @property
    def status(self):
        if self._checkStatus("unknown"):
            return "unknown"
        if self._checkStatus("normal"):
            return "normal"
        return "error"

    @property
    def inspectionStatus(self):
        return self._iccardStatus  

