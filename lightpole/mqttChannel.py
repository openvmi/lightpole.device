import paho.mqtt.client as mqtt
import time

class MqttChannel:
    def __init__(self, deviceId, deviceArea, host, port, onmessage) -> None:
        self._deviceId = deviceId
        self._deviceArea = deviceArea
        self.client = None
        self._host = host
        self._port = port
        self._onmessage = onmessage

    def _onConnect(self, client, userdata, flags, rc):
        self.client = client
        topicPrefix = 'device/' + self._deviceArea + '/' + self._deviceId + '/'
        client.subscribe(topicPrefix + 'request')
        
    def _onDisconnect(self, client, userdata, rc):
        self.client = None

    def run(self):
        while True:
            print(self._host)
            print(self._port)
            _client = mqtt.Client()
            _client.on_connect = self._onConnect
            _client.on_message = self._onmessage
            _client.connect(self._host, self._port)
            _client.loop_forever()
            time.sleep(20)
            print('mqtt reconnect')


    