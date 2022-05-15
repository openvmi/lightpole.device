import json
from pathlib import Path
import os, sys

def getDefault():
    default = {
        "deviceId": "tempId",
        "deviceArea": "tempArea"
    }
    return default

def createDefaultFile():
    home = Path.home()
    vmiDir = home / '.vmi'
    configFile = vmiDir / 'config.json'
    if vmiDir.is_dir() is False:
        vmiDir.mkdir(parents=True, exist_ok=True)

    defaultConfig = getDefault()
    configFile.write_text(json.dumps(defaultConfig, ensure_ascii=False, indent=4), encoding="utf8")
    return defaultConfig

def getConfiguration():
    home = Path.home()
    vmiDir = home / '.vmi'
    configFile = vmiDir / 'config.json'
    if vmiDir.is_dir() is False:
        vmiDir.mkdir(parents=True, exist_ok=True)

    if configFile.is_file() is False:
        return createDefaultFile(), vmiDir
    
    configuration = configFile.read_text()
    try:
        configDict = json.loads(configuration)
    except Exception:
        configDict = createDefaultFile()
    finally:
        return configDict, vmiDir