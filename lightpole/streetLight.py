from unittest import result


class StreetLighting:
    def __init__(self, channel) -> None:
        self._channel = channel
        self._PowserStatus = 'normal'
        self._brightnessStatus = 'normal'
        self._brightness = 0

    @property
    def power(self):
        command = bytes([])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._PowserStatus = 'error'
        else:
            self._PowserStatus = 'normal'
        return result

    @property
    def brightness(self):
        command = bytes([])
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

