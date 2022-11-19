from JsonModel.utility import readJson,writeJson
from datetime import datetime

class JsonModel:
    def __init__(self):
        self.model = {}
    
    def resetModel(self):
        model = readJson("empty.json")
        model["CreatedAt"] = datetime.now().isoformat(timespec='microseconds')
        model["LastModified"] = datetime.now().isoformat(timespec='microseconds')
        self.model = model
        return self.model

    def setLastModified(self):
        self.model["LastModified"] = datetime.now().isoformat(timespec='microseconds')
    
    def saveModel(self):
        return writeJson("Main.json",self.model)