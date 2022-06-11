class WeatherStationDevice:
    def __init__(self, channel) -> None:
        self._channel = channel
        self._windSpeedStatus = "unknown"
        self._temperatureStatus = "unknown"
        self._humidityStatus = "unknown"
        self._illuminanceStatus = "unknown"
        self._noiseStatus = "unknown"
        self._rainStatus = "unknown"
        self._pm2_5Status = "unknown"
        self._pm10Status = "unknown"


    @property
    def windSpeed(self):
        command = bytes([0x02, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x39])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._windSpeedStatus = "error"
        else:
            self._windSpeedStatus = "normal"
        return result

    @property
    def temperature(self):
        command = bytes([0x01, 0x03, 0x01, 0xF5, 0x00, 0x01, 0x95, 0xC4])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._temperatureStatus = "error"
        else:
            self._temperatureStatus = "normal"
        return result

    @property
    def humidity(self):
        command = bytes([0x01, 0x03, 0x01, 0xF4, 0x00, 0x01, 0xC4, 0x04])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._humidityStatus = "error"
        else:
            self._humidityStatus = "normal"
        return result

    @property
    def illuminance(self):
        command = bytes([0x01, 0x03, 0x01, 0xFA, 0x00, 0x02, 0xE5, 0xC6])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._illuminanceStatus = "error"
        else:
            self._illuminanceStatus = "normal"
        return result

    @property
    def moise(self):
        command = bytes([0x01, 0x03, 0x01, 0xF6, 0x00, 0x01, 0x65, 0xC4])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._noiseStatus = "error"
        else:
            self._noiseStatus = "normal"
        return result
    
    @property
    def rain(self):
        command = bytes([0x03, 0x03, 0x00, 0x00, 0x00, 0x01, 0x85, 0xE8])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._rainStatus = "error"
        else:
            self._rainStatus = "normal"
        return result

    @property
    def pm2_5(self):
        command = bytes([0x01, 0x03, 0x01, 0xF7, 0x00, 0x01, 0x34, 0x04])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._pm2_5Status = "error"
        else:
            self._pm2_5Status = "normal"
        return result

    @property
    def pm10(self):
        command = bytes([0x01, 0x03, 0x01, 0xF8, 0x00, 0x01, 0x04, 0x07])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._pm10Status = "error"
        else:
            self._pm10Status = "normal"
        return result


if __name__ == "__main__":
    from .uartChannel import UartChannel
    uartChannel = UartChannel()
    dev = WeatherStationDevice(channel=uartChannel)
    speed = dev.getWindSpeed()
    print(len(speed))
    print(speed)
    

    
