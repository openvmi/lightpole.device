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

        self._workMode = "timer"

    @property
    def iccard(self):
        command = bytes([0x04, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x5E])
        result = self._channel.queryValue(command=command, responseLength=9)  
        if result is None:
            self._iccardStatus = 'error'
        else:
            self._iccardStatus = 'normal'
            result = int(hex(result[5]<<8|result[6]),16)
            result = round(result/1)
        return result

    @property
    def inputvoltage(self):
        command = bytes([0x05, 0x04, 0x00, 0x04, 0x00, 0x01, 0x71, 0x8F])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._inputvoltageStatus = 'error'
        else:
            self._inputvoltageStatus = 'normal'
            result = int(hex(result[3] << 8 | result[4]), 16)
            result = round(result / 10)
        return result

    @property
    def outputcurrent(self):
        command = bytes([0x05, 0x04, 0x00, 0x05, 0x00, 0x01, 0x20, 0x4F])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._outputcurrentStatus = 'error'
        else:
            self._outputcurrentStatus = 'normal'
            result = int(hex(result[3]<<8|result[4]),16)
            result = round(result/1000)
        return result

    @property
    def outputpower(self):
        command = bytes([0x05, 0x04, 0x00, 0x06, 0x00, 0x01, 0xD0, 0x4F])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._outputpowerStatus = 'error'
        else:
            self._outputpowerStatus = 'normal'
            result = int(hex(result[3]<<8|result[4]),16)
            result = round(result/10)
        return result

    @property
    def electricityConsumption(self):
        command = bytes([0x05, 0x04, 0x00, 0x08, 0x00, 0x01, 0xB1, 0x8C])
        result = self._channel.queryValue(command=command, responseLength=7)  
        if result is None:
            self._electricityConsumptionStatus = 'error'
        else:
            self._electricityConsumptionStatus = 'normal'
            result = int(hex(result[3]<<8|result[4]),16)
            result = round(result/1000)
        return result
   
    def crc16(self, x): #modbus协议CRC校验
        a = 0xFFFF
        b = 0xA001
        for byte in x:
            a ^= byte
            for i in range(8):
                last = a % 2
                a >>= 1
                if last == 1:
                    a ^= b
        a=a.to_bytes(2,byteorder='little')
        return a

    @property
    def brightness(self):
        command = bytes([0x05, 0x04, 0x00, 0x06, 0x00, 0x01, 0xD0, 0x4F])
        result = self._channel.queryValue(command=command, responseLength=7)
        if result is None:
            self._brightness = 'error'
        else:
            self._brightness = 'normal'
            result = int(hex(result[3]<<8|result[4]),16)
            result = round(result/1)
        return result

    @brightness.setter
    def brightness(self, value):
        print('trying to set brightness:', value)
        cmd_reg = ['0x05','0x06','0x00','0x04','0x00']
        cmd_reg.append(hex(value))
        cmd_plus = bytearray([int(x,0) for x in cmd_reg])
        cmd_plus = cmd_plus + self.crc16(cmd_plus)
        result = self._channel.queryValue(command=cmd_plus, responseLength=8)
        if result is None:
            self._brightness = 'error'
        else:
            self._brightness = 'normal'
        return result
    
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

if __name__ == "__main__":
    from uartChannel import UartChannel
    import time
    uartChannel = UartChannel(port="COM3")
    dev = StreetLighting(channel=uartChannel)
    while True:
        print(">>>>>>>>开始路灯数据查询>>>>>>>")
        print("iccard:", dev.iccard)
        time.sleep(3)
        print("iccard:", dev.iccard)
        time.sleep(3)
        dev.brightness  = 50
        time.sleep(3)
        print("brightness:", dev.brightness)
        time.sleep(3)
        print("inputvoltage:", dev.inputvoltage)
        time.sleep(3)
        print("outputcurrent:", dev.outputcurrent)
        time.sleep(3)
        print("electricityConsumption:", dev.electricityConsumption)
        time.sleep(3)
        dev.brightness  = 0
        print("brightness:", dev.brightness)
        time.sleep(3)
        
        print("<<<<<<<<<查询结束<<<<<<<<<<<<<")
        print("")
        print("")
        print("")
        time.sleep(5)