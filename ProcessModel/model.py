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
from Transformations.RemoveNullValues import ApplyRemoveNullRows, ApplyRemoveNullColumns
from Transformations.ReplaceNullValues import ReplaceNulls
from Transformations.RemoveOutliers import removeOutliers


class Model:
    def __init__(self):
        self.jsonModel = JM()
        self.df = pd.DataFrame({})
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scores = None
        self.jsonModel.resetModel()
        self.text = ""

    def process(self, text):
        if self.text == text:
            self.text = ""
            ActionItem = detect_intent(text)
            if (ActionItem["Action"] == "DataSelection"):
                self.DataSelection(ActionItem["value"])
            return self.returnRes(ActionItem)
        self.text = text
        ActionItem = detect_intent(text)
        if ActionItem["Action"] == "DataSelection":
            self.DataSelection(ActionItem["value"])
        elif ActionItem["Action"] == "TransformationSelection":
            self.TransformationSelection(
                ActionItem["Selected"], ActionItem["Params"])
        elif ActionItem["Action"] == "ModelSelection":
            self.ModelSelection(ActionItem["value"])
        elif ActionItem["Action"] == "Question":
            pass
        return self.returnRes(ActionItem)

    def returnRes(self, action):
        if action:
            return {"model": self.jsonModel.get(), "Results": self.processJsonModel(),
                    "CurrentProcess": action}
        else:
            return {"model": self.jsonModel.get(), "Results": self.processJsonModel(),
                    "CurrentProcess": {}}

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

    def TransformationSelection(self, selection, params):
        return self.jsonModel.addTransformationBlock(selection, params)

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
                df = ApplyStandardization(df, attributes["Columns"])
            elif attributes["Apply"] == "Normalization":
                df = ApplyNormalization(df)
            elif attributes["Apply"] == "RemoveNullRows":
                df = ApplyRemoveNullRows(df, attributes["Columns"])
            elif attributes["Apply"] == "RemoveNullColumns":
                df = ApplyRemoveNullColumns(df, attributes["Columns"])
            elif attributes["Apply"] == "ReplaceNullValues":
                df = ReplaceNulls(
                    df, attributes["Columns"], attributes["ReplaceWith"])
            elif attributes["Apply"] == "RemoveOutliers":
                df = removeOutliers(df, attributes["Option"])
            elif attributes["Apply"] == "SplitTrainTest":
                X = df[list(df.columns[:-1])]
                y = list(df[df.columns[-1]])
                self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                    X, y, test_size=0.20, random_state=42)
        self.df = df

    def processMlModel(self, block):
        attributes = self.processComplexJson(block["Attributes"])
        if "Apply" in attributes:
            if attributes["Apply"] == "LinearRegression":
                response = LinearRegressionModel(
                    self.X_train, self.X_test, self.y_train, self.y_test)
                print(response["Scores"])
                self.scores = response["Scores"]
            else:
                response = DecissionTreeModel(
                    self.X_train, self.X_test, self.y_train, self.y_test)
                self.scores = response["Scores"]
                print(response["Scores"])

    def Results(self):
        # if self.scores is not None:
        #     return self.scores
        # if self.X_train is not None or self.X_test is not None or self.y_train is not None or self.y_test is not None:
        #     result_X_train = self.X_train.head(2).to_json(orient="index")
        #     result_y_train = self.y_train[:2]
        #     result_X_test = self.X_test.head(2).to_json(orient="index")
        #     result_y_test = self.y_test[:2]
        #     return {
        #         "X_train": json.loads(result_X_train),
        #         "y_train": result_y_train,
        #         "X_test": json.loads(result_X_test),
        #         "y_test": result_y_test
        #     }
        result = self.df.head(3).to_json(orient="index")
        columns = list(self.df.columns)
        parsed = json.loads(result)
        results = [parsed[i] for i in list(parsed.keys())]
        results.insert(0, columns)
        return results

    def ResetModel(self):
        self.jsonModel = JM()
        self.df = pd.DataFrame({})
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scores = None
        self.jsonModel.resetModel()
        return self.jsonModel.get()
