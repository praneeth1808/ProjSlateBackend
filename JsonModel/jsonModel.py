from JsonModel.utility import readJson, writeJson
from datetime import datetime
import uuid


class JsonModel:
    def __init__(self):
        self.model = {}
        self.initiate()

    def resetModel(self):
        model = readJson("empty.json")
        model["CreatedAt"] = datetime.now().isoformat(timespec='microseconds')
        model["LastModified"] = datetime.now(
        ).isoformat(timespec='microseconds')
        self.model = model
        return self.model

    def setLastModified(self):
        self.model["LastModified"] = datetime.now(
        ).isoformat(timespec='microseconds')

    def saveModel(self):
        return writeJson("Main.json", self.model)

    def addBlock(self, block):
        self.model["Blocks"].append(block)
        return self.model

    def get(self):
        return self.model

    def initiate(self):
        model = readJson("Main.json")
        self.model = model

    def addDataBlock(self, dataset):
        self.resetModel()
        block = {
            "id": uuid.uuid4(),
            "Category": "Data",
            "Attributes": []

        }
        if dataset == "Iris":
            block["Attributes"].append({
                "key": "DataSet",
                "value": "Iris"
            })
            block["Attributes"].append({
                "key": "filename",
                "value": "iris.csv"
            })
        else:
            block["Attributes"].append({
                "key": "DataSet",
                "value": "Titanic"
            })
            block["Attributes"].append({
                "key": "filename",
                "value": "titanic.csv"
            })
        self.addBlock(block)
