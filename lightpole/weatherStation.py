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
            result = 0
        else:
            self._windSpeedStatus = "normal"
            print("windSpeed", result)
            result = int(hex(result[3]<<8|result[4]),16)
            result = round(result/10)
        return result

    @property
    def temperature(self):
        command = bytes([0x06, 0x03, 0x01, 0xF5, 0x00, 0x01, 0x94, 0x73])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._temperatureStatus = "error"
            result = 0
        else:
            self._temperatureStatus = "normal"
            print("temperature:",result)
            result = int(hex(result[3]<<8|result[4]),16)
            result = round(result/10)
        return result

    @property
    def humidity(self):
        command = bytes([0x06, 0x03, 0x01, 0xF4, 0x00, 0x01, 0xC5, 0xB3])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._humidityStatus = "error"
            result = 0
        else:
            self._humidityStatus = "normal"
            result = int(hex(result[3]<<8|result[4]),16)
            result = round(result/10)
        return result

    @property
    def illuminance(self):
        command = bytes([0x06, 0x03, 0x01, 0xFA, 0x00, 0x02, 0xE4, 0x71])
        result = self._channel.queryValue(command=command, responseLength=9)
        if result is None:
            self._illuminanceStatus = "error"
            result = 0
        else:
            self._illuminanceStatus = "normal"
            result = int(hex(result[5]<<8|result[6]),16)
            result = round(result/10)
        return result

    @property
    def noise(self):
        command = bytes([0x06, 0x03, 0x01, 0xF6, 0x00, 0x01, 0x64, 0x73])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._noiseStatus = "error"
            result = 0
        else:
            self._noiseStatus = "normal"
            result = int(hex(result[3]<<8|result[4]),16)
            result = round(result/10)
        return result
    
    @property
    def rain(self):
        command = bytes([0x03, 0x03, 0x00, 0x00, 0x00, 0x01, 0x85, 0xE8])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._rainStatus = "error"
            result = 0
        else:
            self._rainStatus = "normal"
            result = int(hex(result[3]<<8|result[4]),16)
            result = round(result/1)
        return result

    @property
    def pm2_5(self):
        command = bytes([0x06, 0x03, 0x01, 0xF7, 0x00, 0x01, 0x35, 0xB3])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._pm2_5Status = "error"
            result = 0
        else:
            self._pm2_5Status = "normal"
            result = int(hex(result[3]<<8|result[4]),16)
            result = round(result/1)
        return result

    @property
    def pm10(self):
        command = bytes([0x06, 0x03, 0x01, 0xF8, 0x00, 0x01, 0x05, 0xB0])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._pm10Status = "error"
            result = 0
        else:
            self._pm10Status = "normal"
            result = int(hex(result[3]<<8|result[4]),16)
            result = round(result/1)
        return result

    @property
    def carbonDioxide(self):
        return 0

    def _checkStatus(self, status):
        if self._windSpeedStatus == status and \
            self._temperatureStatus == status and \
            self._humidityStatus == status and \
            self._illuminanceStatus == status and \
            self._noiseStatus == status and \
            self._rainStatus == status and \
            self._pm2_5Status == status and \
            self._pm10Status == status:
            return True
            
    @property
    def status(self):
        if self._checkStatus("unknown"):
            return "unknown"
        if self._checkStatus("normal"):
            return "normal"
        return "error"                                                                        


if __name__ == "__main__":
    from uartChannel import UartChannel
    import time
    uartChannel = UartChannel(port="COM3")
    dev = WeatherStationDevice(channel=uartChannel)
    while True:
        print(">>>>>>>>开始气象站数据查询>>>>>>>")
        print("windSpeed:", dev.windSpeed)
        time.sleep(2)
        print("temperature:", dev.temperature)
        time.sleep(2)
        print("humidity:", dev.humidity)
        time.sleep(2)
        print("illuminance:", dev.illuminance)
        time.sleep(2)
        print("noise:", dev.noise)
        time.sleep(2)
        print("rain:", dev.rain)
        time.sleep(2)
        print("pm2_5:", dev.pm2_5)
        time.sleep(2)
        print("pm10:", dev.pm10)
        time.sleep(2)
        print("carbonDioxide:", dev.carbonDioxide)
        print("<<<<<<<<<气象站查询结束<<<<<<<<<<<<<")
        print("")
        print("")
        print("")
        time.sleep(6)
    
