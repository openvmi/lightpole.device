from unittest import result


class StreetLighting:
    def __init__(self, channel) -> None:
        self._channel = channel
        self._PowserStatus = 'normal'
        self._brightnessStatus = 'normal'
        self._brightness = 0

    @property
    def iccard(self):
        command = bytes([0x04, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x5E])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._PowserStatus = 'error'
        else:
            self._PowserStatus = 'normal'
        return result

    @property
    def inputvoltage(self):
        command = bytes([0x05, 0x04, 0x00, 0x04, 0x00, 0x01, 0x71, 0x8F])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._PowserStatus = 'error'
        else:
            self._PowserStatus = 'normal'
        return result

    @property
    def outputcurrent(self):
        command = bytes([0x05, 0x04, 0x00, 0x05, 0x00, 0x01, 0x20, 0x4F])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._PowserStatus = 'error'
        else:
            self._PowserStatus = 'normal'
        return result

    @property
    def outputpower(self):
        command = bytes([0x05, 0x04, 0x00, 0x06, 0x00, 0x01, 0xD0, 0x4F])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._PowserStatus = 'error'
        else:
            self._PowserStatus = 'normal'
        return result

    @property
    def Electricityconsumption(self):
        command = bytes([0x05, 0x04, 0x00, 0x08, 0x00, 0x01, 0xB1, 0x8C])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._PowserStatus = 'error'
        else:
            self._PowserStatus = 'normal'
        return result
   

    @property
    def brightness(self):
        command = bytes([0x05, 0x06, 0x00, 0x04, 0x00, 0x32, 0x48, 0x5A])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._brightness = 'error'
        else:
            self._brightness = 'normal'
        return result

    @brightness.setter
    def brightness(self, value):
        print('trying to set brightness')
        self._brightness = value

