from JsonModel.jsonModel import JsonModel as JM
from detectIntent import detect_intent
import pandas as pd


class Model:
    def __init__(self):
        self.jsonModel = JM()
        self.df = pd.DataFrame({})

    def process(self, text):
        ActionItem = detect_intent(text)
        if ActionItem["Action"] == "DataSelection":
            self.DataSelection(ActionItem["value"])
        return self.jsonModel.get()

    def processJsonModel(self):
        model_json = self.jsonModel.get()
        return model_json

    def Results(self):
        return {"Accuracy": 95, "R2": 0.89}

    def getModel(self):
        return self.jsonModel.model

    def DataSelection(self, dataset):
        return self.jsonModel.addDataBlock(dataset)
