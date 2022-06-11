import sys
from .mqttChannel import MqttChannel
from .protocol import Protocol
from .weatherStation import WeatherStationDevice
from .streetLight import StreetLighting
from .uartChannel import UartChannel
import threading
import time
import json


class App:
    def __init__(self, mqttHost, mqttPort, uartPort='/dev/ttyUSB0', 
                        uartBaudrate=9600,
                        uartTimeout=3,
                        deviceId = 'tempId1',
                        deviceArea= 'tempArea',) -> None:
        self._mqttHost = mqttHost
        self._mqttPort = mqttPort
        self._uartPort = uartPort
        self._uartBaudrate = uartBaudrate
        self._uartTimeout = uartTimeout
        self._deviceId = deviceId
        self._deviceArea = deviceArea

        self._uart = UartChannel()
        self._weatherStation = WeatherStationDevice(channel=self._uart)
        self._streetLight = StreetLighting(channel=self._uart)
        self._mqtt = MqttChannel(deviceId=self._deviceId, deviceArea=self._deviceArea, host=self._mqttHost, port=self._mqttPort,onmessage=self._onMessage)
        self._mqttThread = None

        self._pingDuration = 10
        self._pingTopic = 'device/' + self._deviceArea + '/' + self._deviceId + '/ping'

        self._notifySensorStatusDuration = 30
        self._notifySensorStatusTopic = 'device/' + self._deviceArea + '/' + self._deviceId + '/notify'

    def _getPingMsg(self):
        proto = Protocol(deviceId=self._deviceId, deviceArea=self._deviceArea)
        return proto.getPingInJson()
  
    def _getNotifySensorStatusMsg(self):
        proto = Protocol(deviceId=self._deviceId, deviceArea=self._deviceArea)
        return proto.getDataInJson()
        
    def run(self):
        if self._mqttThread is not None:
            return
        self._mqttThread = threading.Thread(name='mqttThread', target=self._mqtt.run, daemon=True)
        self._mqttThread.start()
        sleepCount = 10
        while True:
            if sleepCount >= self._pingDuration and sleepCount % self._pingDuration  == 0:
                print("send ping")
                ping = self._getPingMsg()
                client = self._mqtt.client
                if ping is not None and client is not None:
                    self._mqtt.client.publish(self._pingTopic, payload=json.dumps(ping))
            if sleepCount >= self._notifySensorStatusDuration and sleepCount % self._notifySensorStatusDuration == 0:
                print("send notify")
                notify = self._getNotifySensorStatusMsg()
                client = self._mqtt.client
                if notify is not None and client is not None:
                    self._mqtt.client.publish(self._notifySensorStatusTopic, payload=json.dumps(notify))
            time.sleep(1)
            sleepCount = sleepCount + 1
            if sleepCount > sys.maxsize - 10:
                sleepCount = 0


    def _onMessage(self, client, userdata, msg):
        print(msg.topic)
        print(msg.payload)
        print(msg.qos)
        print(msg.retain)