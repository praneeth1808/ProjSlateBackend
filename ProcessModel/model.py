from JsonModel.jsonModel import JsonModel as JM
from JsonModel.utility import getDataFilePath
from MLModel.DecissionTree import DecissionTreeModel
from MLModel.LinearRegression import LinearRegressionModel
from detectIntent import detect_intent
import pandas as pd
import json
from Transformations.Standardization import ApplyStandardization
from Transformations.Normalization import ApplyNormalization
from sklearn.model_selection import train_test_split


class Model:
    def __init__(self):
        self.jsonModel = JM()
        self.df = pd.DataFrame({})
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scores = None

    def process(self, text):
        ActionItem = detect_intent(text)
        if ActionItem["Action"] == "DataSelection":
            self.DataSelection(ActionItem["value"])
        elif ActionItem["Action"] == "TransformationSelection":
            self.TransformationSelection(ActionItem["Selected"])
        elif ActionItem["Action"] == "ModelSelection":
            self.ModelSelection(ActionItem["value"])
        self.processJsonModel()
        return {"model": self.jsonModel.get(), "Results": self.processJsonModel(), "CurrentProcess": ActionItem}

    def processJsonModel(self):
        model_json = self.jsonModel.get()
        for block in model_json["Blocks"]:
            if block["Category"] == "Data":
                self.processDataBlock(block)
            elif block["Category"] == "Transform":
                self.processTransformBlock(block)
            elif block["Category"] == "Model":
                self.processMlModel(block)
        return self.Results()

    def getModel(self):
        return self.jsonModel.model

    def DataSelection(self, dataset):

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scores = None
        return self.jsonModel.addDataBlock(dataset)

    def TransformationSelection(self, selection):
        return self.jsonModel.addTransformationBlock(selection)

    def ModelSelection(self, selection):
        return self.jsonModel.addModelBlock(selection)

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
        if "Apply" in attributes:
            if attributes["Apply"] == "Standardization":
                df = ApplyStandardization(df)
            elif attributes["Apply"] == "Normalization":
                df = ApplyNormalization(df)
            elif attributes["Apply"] == "SplitTrainTest":
                X = df[list(df.columns[:-1])]
                y = list(df[df.columns[-1]])
                print(y)
                self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                    X, y, test_size=0.20, random_state=42)
        self.df = df

    def processMlModel(self, block):
        attributes = self.processComplexJson(block["Attributes"])
        if "Apply" in attributes:
            if attributes["Apply"] == "LinearRegression":
                response = LinearRegressionModel(
                    self.X_train, self.X_test, self.y_train, self.y_test)
                self.scores = response["Scores"]
            else:
                response = DecissionTreeModel(
                    self.X_train, self.X_test, self.y_train, self.y_test)
                self.scores = response["Scores"]

    def Results(self):
        if self.scores is not None:
            return self.scores
        if self.X_train is not None or self.X_test is not None or self.y_train is not None or self.y_test is not None:
            result_X_train = self.X_train.head(2).to_json(orient="index")
            result_y_train = self.y_train[:2]
            result_X_test = self.X_test.head(2).to_json(orient="index")
            result_y_test = self.y_test[:2]
            return {
                "X_train": json.loads(result_X_train),
                "y_train": result_y_train,
                "X_test": json.loads(result_X_test),
                "y_test": result_y_test
            }
        result = self.df.head(3).to_json(orient="index")
        parsed = json.loads(result)
        return parsed
