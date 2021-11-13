def loadConfig(configFile):
    config = {  }

    lines = configFile.readlines()
    for line in lines:
        name, path = line.replace('\n', '').split(':')

        with open(path, 'r') as reader:
            config[name] = reader.read()

    return config

def getConfig(path):
    with open(path, 'r') as file:
        return loadConfig(file)