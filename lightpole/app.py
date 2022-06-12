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

        self._streetLightWorkThread = None
        self._streetLightWorkMode = "manual"
        self._quitTask = True

    '''
    startDate:{hour:12, minute: 23}
    duration: {hourDuration:15, minuteDuration: 43}
    '''
    def _timerModeTask(self,startDate, duration):
        endMinutes = startDate.minute + duration.minuteDuration
        endHour = startDate.hour + duration.hourDuration
        hasNextDay = False
        if endMinutes >= 60:
            endHour = endHour + 1
            endMinutes = endMinutes % 60
        if endHour >= 24:
            hasNextDay = True
            endHour = endHour % 24
        while self._quitTask is False:
            time.sleep(10)
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            if hasNextDay is True:
                if hour >= startDate.hour and minute >= startDate.minute:
                    self._streetLight.brightness = 100
                elif hour <= endHour and minute <= endMinutes:
                    self._streetLight.brightness = 100
                else:
                    self._streetLight.brightness = 0
            
            if hasNextDay is False:
                if hour < startDate.hour:
                    self._streetLight.brightness = 0
                elif hour == startDate.hour and minute <= startDate.minute:
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
        return proto.getDataInJson()

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
        startDate = {
            "hour": 19,
            "minute": 0
        }
        duration = {
            "hourDuration": 9,
            "minuteDuration": 0
        }
        self._quitTask = True
        self._streetLightWorkThread = threading.Thread(name="streetThread",target=self._timerModeTask,args=(startDate, duration))
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