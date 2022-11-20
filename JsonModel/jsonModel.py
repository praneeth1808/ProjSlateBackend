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
        self.setLastModified()
        return writeJson("Main.json", self.model)

    def addBlock(self, block):
        self.model["Blocks"].append(block)
        self.saveModel()
        return self.model

    def get(self):
        return self.model

    def initiate(self):
        model = readJson("Main.json")
        self.model = model

    def addDataBlock(self, dataset):
        self.resetModel()
        block = {
            "id": str(uuid.uuid4()),
            "Category": "Data",
            "Attributes": []

        }
        if dataset == "Iris":
            block["Attributes"].append({
                "key": "Description",
                "value": "The Iris Dataframe"
            })
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
                "key": "Description",
                "value": "The Boston Dataframe"
            })
            block["Attributes"].append({
                "key": "DataSet",
                "value": "Boston"
            })
            block["Attributes"].append({
                "key": "filename",
                "value": "boston.csv"
            })
        self.addBlock(block)

    def addTransformationBlock(self, selection):
        block = {
            "id": str(uuid.uuid4()),
            "Category": "Transform",
            "Attributes": []
        }
        if selection == "ApplyStandardization":
            block["Attributes"].append({
                "key": "Description",
                "value": "This block applies Standerdisation to the dataframe."
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "Standardization"
            })
        elif selection == "ApplyNormalization":
            block["Attributes"].append({
                "key": "Description",
                "value": "This block applies Standerdisation to the dataframe."
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "Normalization"
            })
        elif selection == "ApplySplitTrainTest":
            block["Attributes"].append({
                "key": "Description",
                "value": "This block applies Split into train and test into 80-20%"
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "SplitTrainTest"
            })
        else:
            block["Attributes"].append({
                "key": "Description",
                "value": "This block applies Standerdisation to the dataframe."
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "None"
            })
        self.addBlock(block)

    def addModelBlock(self, selectedModel):
        block = {
            "id": str(uuid.uuid4()),
            "Category": "Model",
            "Attributes": []
        }
        if selectedModel == "Linear Regression":
            block["Attributes"].append({
                "key": "Description",
                "value": "This block performs ML operation Linear Regression"
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "LinearRegression"
            })
        else:
            block["Attributes"].append({
                "key": "Description",
                "value": "This block performs ML operation Decission Tree"
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "DecissionTree"
            })
        self.addBlock(block)
