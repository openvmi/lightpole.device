import serial

class Device:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=3) -> None:
        self._baudrate = baudrate
        self._port = port
        self._timeout = timeout
        self._serial = None
    
    def _queryValue(self, command, responseLength):
        if self._serial is None or self._serial.is_open is False:
            try:
                self._serial = serial.Serial(self._port, self._baudrate, timeout=self._timeout)
            except serial.SerialException:
                return None
        try:
            self._serial.write(command)
        except serial.SerialTimeoutException:
            return None
        value = self._serial.read(responseLength)
        return value

    def getWindSpeed(self):
        command = bytes([0x01, 0x03, 0x00, 0x09, 0x00, 0x01, 0x54, 0x08])
        result = self._queryValue(command=command, responseLength=7)
        return result


if __name__ == "__main__":
    dev = Device()
    speed = dev.getWindSpeed()
    print(len(speed))
    print(speed)
    

    