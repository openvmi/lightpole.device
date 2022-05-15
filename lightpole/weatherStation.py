from tkinter.messagebox import NO
import serial

class WeatherStationDevice:
    def __init__(self, channel) -> None:
        self._channel = channel
        self._status = "normal"

    def getWindSpeed(self):
        command = bytes([0x01, 0x03, 0x00, 0x09, 0x00, 0x01, 0x54, 0x08])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._status = "error"
        return result


if __name__ == "__main__":
    from .uartChannel import UartChannel
    uartChannel = UartChannel()
    dev = WeatherStationDevice(channel=uartChannel)
    speed = dev.getWindSpeed()
    print(len(speed))
    print(speed)
    

    