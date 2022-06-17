import sys
from .mqttChannel import MqttChannel
from .protocol import Protocol
from .weatherStation import WeatherStationDevice
from .streetLight import StreetLighting
from .uartChannel import UartChannel
import threading
import time
import json

from datetime import datetime
class App:
    def __init__(self, mqttHost, mqttPort, uartPort='/dev/ttyUSB0', 
                        uartBaudrate=9600,
                        uartTimeout=3,
                        deviceId = 'tempId1',
                        deviceArea= 'tempArea',
                        mqttConfig = None) -> None:
        self._mqttHost = mqttHost
        self._mqttPort = mqttPort
        self._mqttConfig = mqttConfig

        self._uartPort = uartPort
        self._uartBaudrate = uartBaudrate
        self._uartTimeout = uartTimeout
        self._deviceId = deviceId
        self._deviceArea = deviceArea

        self._uart = UartChannel()
        self._weatherStation = WeatherStationDevice(channel=self._uart)
        self._streetLight = StreetLighting(channel=self._uart)
        self._mqtt = MqttChannel(deviceId=self._deviceId,
            deviceArea=self._deviceArea,
            host=self._mqttHost,
            port=self._mqttPort,
            onmessage=self._onMessage,
            configuration=self._mqttConfig)

        self._mqttThread = None

        self._pingDuration = 10
        self._pingTopic = 'device/' + self._deviceArea + '/' + self._deviceId + '/ping'

        self._notifySensorStatusDuration = 30
        self._notifySensorStatusTopic = 'device/' + self._deviceArea + '/' + self._deviceId + '/notify'

        self._streetLightWorkThread = None
        self._streetLightWorkMode = "manual"
        self._streetLightTimerEvent = threading.Event()
        self._streetLightTimerEvent.set()
        self._streetLighterTimerStartDate = {
            "hour": 19,
            "minute": 0
        }
        self._streetLighterTimerDuration = {
            "hourDuration": 9,
            "minuteDuration": 0
        }
        self._quitTask = True

    '''
    self._streetLighterTimerStartDate:{hour:12, minute: 23}
    duration: {hourDuration:15, minuteDuration: 43}
    '''
    def _timerModeTask(self):
        while True:
            time.sleep(10)
            if not self._streetLightTimerEvent.is_set():
                continue
            endMinutes = self._streetLighterTimerStartDate["minute"] + self._streetLighterTimerDuration["minuteDuration"]
            endHour = self._streetLighterTimerStartDate["hour"] + self._streetLighterTimerDuration["hourDuration"]
            hasNextDay = False
            if endMinutes >= 60:
                endHour = endHour + 1
                endMinutes = endMinutes % 60
            if endHour >= 24:
                hasNextDay = True
                endHour = endHour % 24
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            if hasNextDay is True:
                if hour == self._streetLighterTimerStartDate["hour"] and minute >= self._streetLighterTimerStartDate["minute"]:
                    self._streetLight.brightness = 100
                elif hour > self._streetLighterTimerStartDate["hour"]:
                    self._streetLight.brightness = 100
                elif hour == endHour and minute <= endMinutes:
                    self._streetLight.brightness = 100
                elif hour < endHour:
                    self._streetLight = 100
                else:
                    self._streetLight.brightness = 0
            
            if hasNextDay is False:
                if hour < self._streetLighterTimerStartDate["hour"]:
                    self._streetLight.brightness = 0
                elif hour == self._streetLighterTimerStartDate["hour"] and minute <= self._streetLighterTimerStartDate["minute"]:
                    self._streetLight.brightness = 0
                elif hour > endHour:
                    self._streetLight.brightness = 0
                elif hour == endHour and minute >= endMinutes:
                    self._streetLight.brightness = 0
                else:
                    self._streetLight.brightness = 100


    def _getPingMsg(self):
        proto = Protocol(deviceId=self._deviceId, deviceArea=self._deviceArea)
        proto.setEmergencyPowerStatus("normal")
        proto.setWeatherStationStatus(self._weatherStation.status)
        proto.setStreetLightingStatus(self._streetLight.status)
        proto.setInspectionStatus(self._streetLight.inspectionStatus)
        return proto.getPingInJson()
  
    def _getNotifySensorStatusMsg(self):
        proto = Protocol(deviceId=self._deviceId, deviceArea=self._deviceArea)
        proto.temperature = self._weatherStation.temperature
        proto.humidity = self._weatherStation.humidity
        proto.illuminance = self._weatherStation.illuminance
        proto.noise = self._weatherStation.noise
        proto.windsSpeed = self._weatherStation.windSpeed
        proto.rain = self._weatherStation.rain
        proto.pm2_5 = self._weatherStation.pm2_5
        proto.pm10 = self._weatherStation.pm10
        proto.carbonDioxide = self._weatherStation.carbonDioxide
        proto.power = self._streetLight.electricityConsumption
        proto.lightingLevel = self._streetLight.brightness
        proto.workMode = self._streetLight._workMode
        proto.lightingStatus = "normal"
        return proto.getSensorStatusInJson()

    def _getInspectionStatusMsg(self):
        proto = Protocol(deviceId=self._deviceId, deviceArea=self._deviceArea)
        proto.employeeID = self._streetLight.iccard
        proto.employeeName = "unknown"
        proto.employeeTemperature = 28
        return proto.getInspectionStatusInJson()

    def run(self):
        if self._mqttThread is not None:
            return
        self._mqttThread = threading.Thread(name='mqttThread', target=self._mqtt.run, daemon=True)
        self._mqttThread.start()
        self._streetLightWorkThread = threading.Thread(name="streetThreadTimer",target=self._timerModeTask)
        self._streetLightWorkThread.start()

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