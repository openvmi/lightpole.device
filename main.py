from lightpole.app import App
from lightpole.config import getConfiguration

def main():
    configuration, logDir = getConfiguration()
    deviceId = configuration.get('deviceId', 'tempId')
    deviceArea = configuration.get('deviceArea', 'tempArea')
    mqttHost = configuration.get('host', None)
    mqttPort = configuration.get('port', None)
    mqttUser = configuration.get("user", None)
    mqttPwd = configuration.get("pwd",None)

    print(configuration)
    print(logDir)
    
    if mqttHost is None or mqttPort is None:
        print('Please provide valid mqtt host and port')
        exit(1)
    config = None
    if mqttUser is not None and mqttPwd is not None:
        config = {
            "username": mqttUser,
            "password": mqttPwd
        }
    app = App(mqttHost=mqttHost,
        mqttPort=mqttPort,
        deviceId=deviceId,
        deviceArea=deviceArea,
        mqttConfig=config)
    app.run()


if __name__ == "__main__":
    main()