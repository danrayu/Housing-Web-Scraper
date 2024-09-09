import json

def readConfig(config_path):
  with open(config_path, 'r') as file:
    return json.load(file)
    