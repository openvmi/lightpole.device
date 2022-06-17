from matplotlib.style import use
import paho.mqtt.client as mqtt
import time
import json

class MqttChannel:
    def __init__(self, deviceId, deviceArea, host, port, onmessage, configuration=None) -> None:
        self._deviceId = deviceId
        self._deviceArea = deviceArea
        self.client = None
        self._host = host
        self._port = port
        self._configuration = configuration
        self._onmessage = onmessage

    def _onConnect(self, client, userdata, flags, rc):
        print("connected")
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
            if self._configuration is not None:
                _client.username_pw_set(username=self._configuration["username"],password=self._configuration["password"])
            _client.connect(self._host, self._port)
            _client.loop_forever()
            time.sleep(20)
            print('mqtt reconnect')


if __name__ == "__main__":
    def onmessage(client, userdata, msg):
        print(msg.topic)
        print(json.loads(msg.payload))
        print(msg.qos)
        print(msg.retain)
    confg = {
        "username": "user",
        "password": "password"
    }
    mqttobj = MqttChannel(deviceId="tempid",
        deviceArea="temparea",
        host="192.168.0.107",
        port=1883,
        onmessage=onmessage,
        configuration=confg)
    mqttobj.run()

     