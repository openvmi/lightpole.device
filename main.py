from email.policy import default
from lightpole.app import App
from lightpole.config import getConfiguration

def main():
    configuration, logDir = getConfiguration()
    deviceId = configuration.get('deviceId', 'tempId')
    deviceArea = configuration.get('deviceArea', 'tempArea')
    mqttHost = configuration.get('host', None)
    mqttPort = configuration.get('port', None)

    if mqttHost is None or mqttPort is None:
        print('Please provide valid mqtt host and port')
        exit(1)
    app = App(mqttHost=mqttHost, mqttPort=mqttPort, deviceId=deviceId, deviceArea=deviceArea)
    app.run()
    print(configuration)
    print(logDir)


if __name__ == "__main__":
    main()