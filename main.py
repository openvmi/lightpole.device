from matplotlib.colors import LightSource
from lightpole.app import App
from lightpole.config import getConfiguration
import lightpole

def main():
    configuration, logDir = getConfiguration()
    deviceId = configuration.get('deviceId', 'tempId')
    deviceArea = configuration.get('deviceArea', 'tempArea')
    mqttHost = configuration.get('host', None)
    mqttPort = configuration.get('port', None)
    mqttUser = configuration.get("user", None)
    mqttPwd = configuration.get("pwd",None)

    enableConsole = configuration.get("consoleLog", None)
    enableFileLog = configuration.get("fileLog", None)
    logLevel = configuration.get('logLevel', "warning")

    print(configuration)
    print(logDir)
    
    if enableConsole is not None and enableConsole.lower() == "enable":
        lightpole.enableConsoleHandler()
    
    if enableFileLog is not None and enableFileLog.lower() == "enable":
        lightpole.enableFileHandler()
    lightpole.setLogLevel(logLevel)
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