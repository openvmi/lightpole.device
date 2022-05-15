import serial

class UartChannel:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=3) -> None:
        self._baudrate = baudrate
        self._port = port
        self._timeout = timeout
        self._serial = None
    
    def queryValue(self, command, responseLength):
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