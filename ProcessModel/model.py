from JsonModel.jsonModel import JsonModel as JM
from JsonModel.utility import getDataFilePath
from detectIntent import detect_intent
import pandas as pd
import json
from Transformations.Standardization import ApplyStandardization
from Transformations.Normalization import ApplyNormalization


class Model:
    def __init__(self):
        self.jsonModel = JM()
        self.df = pd.DataFrame({})

    def process(self, text):
        ActionItem = detect_intent(text)
        if ActionItem["Action"] == "DataSelection":
            self.DataSelection(ActionItem["value"])
        elif ActionItem["Action"] == "TransformationSelection":
            self.TransformationSelection(ActionItem["Selected"])
        self.processJsonModel()
        return {"model": self.jsonModel.get(), "Results": self.processJsonModel(), "CurrentProcess": ActionItem}

    def processJsonModel(self):
        model_json = self.jsonModel.get()
        for block in model_json["Blocks"]:
            if block["Category"] == "Data":
                self.processDataBlock(block)
            elif block["Category"] == "Transform":
                self.processTransformBlock(block)
        return self.Results()

    def getModel(self):
        return self.jsonModel.model

    def DataSelection(self, dataset):
        return self.jsonModel.addDataBlock(dataset)

    def TransformationSelection(self, selection):
        return self.jsonModel.addTransformationBlock(selection)

    def processComplexJson(self, json):
        result = {}
        for attribure in json:
            result[attribure["key"]] = attribure["value"]
        return result

    def processDataBlock(self, block):
        attributes = self.processComplexJson(block["Attributes"])
        self.df = pd.read_csv(getDataFilePath(attributes["filename"]))

    def processTransformBlock(self, block):
        attributes = self.processComplexJson(block["Attributes"])
        df = self.df.copy()
        if attributes["Apply"] == "Standardization":
            df = ApplyStandardization(df)
        elif attributes["Apply"] == "Normalization":
            df = ApplyNormalization(df)

        self.df = df
        # self.df = pd.read_csv(getDataFilePath(attributes["filename"]))

    def Results(self):
        result = self.df.head(3).to_json(orient="index")
        parsed = json.loads(result)
        return parsed
