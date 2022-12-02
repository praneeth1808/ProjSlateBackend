from JsonModel.utility import readJson, writeJson
from datetime import datetime
import uuid


def processComplexJson(json):
    result = {}
    for attribure in json:
        result[attribure["key"]] = attribure["value"]
    return result


class JsonModel:
    def __init__(self):
        self.model = {}
        self.initiate()
        self.dataName = "Iris"

    def resetModel(self):
        model = readJson("empty.json")
        model["CreatedAt"] = datetime.now().isoformat(timespec='microseconds')
        model["LastModified"] = datetime.now(
        ).isoformat(timespec='microseconds')
        self.model = model
        self.saveModel()
        return self.model

    def setLastModified(self):
        self.model["LastModified"] = datetime.now(
        ).isoformat(timespec='microseconds')

    def saveModel(self):
        self.setLastModified()
        self.rearrangeBlocks()
        return writeJson("Main.json", self.model)

    def addBlock(self, block):
        self.model["Blocks"].append(block)

        self.saveModel()
        return self.model

    def rearrangeBlocks(self):
        dataBlock = None
        MLBlock = None
        EntireBlocks = []
        for index, block in enumerate(self.model["Blocks"]):
            if block["Category"] == "Model":
                MLBlock = block
            elif block["Category"] == "Data":
                dataBlock = block
            else:
                EntireBlocks.append(block)
        if (dataBlock):
            EntireBlocks.insert(0, dataBlock)
        if (MLBlock):
            EntireBlocks.append(MLBlock)
        self.model["Blocks"] = EntireBlocks

    def updateBlock(self, block):
        for index, oldBlock in enumerate(self.model["Blocks"]):
            if block["id"] == oldBlock["id"]:
                self.model["Blocks"][index] = block
        self.saveModel()
        return self.model

    def remove(self, index):
        blocks = self.model["Blocks"]
        blocks.pop(index-1)
        self.model["Blocks"] = blocks

    def get(self):
        return self.model

    def initiate(self):
        try:
            model = readJson("Main.json")
        except:
            self.resetModel()
            model = readJson("Main.json")
        self.model = model

    def addDataBlock(self, dataset):
        self.resetModel()
        block = {
            "id": str(uuid.uuid4()),
            "Category": "Data",
            "Attributes": []

        }
        self.dataName = dataset
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
                "value": "The sales dataset"
            })
            block["Attributes"].append({
                "key": "DataSet",
                "value": "Sales"
            })
            block["Attributes"].append({
                "key": "filename",
                "value": "advertising.csv"
            })
        self.addBlock(block)

    def addTransformationBlock(self, selection, params):
        option = None
        if params:
            if "replaceoptions" in params:
                option = params["replaceoptions"]
        block = self.isBlockExist(selection, option)
        if block:
            if "Selected" in selection:
                columns = self.SelectCols(self.dataName, params)
            else:
                columns = "All"
            if selection == "RemoveOutliers":
                block, message = self.ModifyTheExistingBlock(
                    block, columns, params["OutliersOptions"])
            else:
                block, message = self.ModifyTheExistingBlock(
                    block, columns, None, params)
            self.updateBlock(block)
            return self.model
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
            block["Attributes"].append({
                "key": "Columns",
                "value": "All"
            })
        elif selection == "ApplySelectedStandardization":
            block["Attributes"].append({
                "key": "Description",
                "value": "This block applies Standerdisation to the dataframe."
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "Standardization"
            })
            columns = self.SelectCols(self.dataName, params)
            block["Attributes"].append({
                "key": "Columns",
                "value": columns
            })
        elif selection == "ApplyNormalization":
            block["Attributes"].append({
                "key": "Description",
                "value": "This block applies Normalization to the dataframe."
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "Normalization"
            })
            block["Attributes"].append({
                "key": "Columns",
                "value": "All"
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
        elif selection == "RemoveNullRows":
            block["Attributes"].append({
                "key": "Description",
                "value": "This block Removes Null rows"
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "RemoveNullRows"
            })
            block["Attributes"].append({
                "key": "Columns",
                "value": "All"
            })
        elif selection == "RemoveNullColumns":
            block["Attributes"].append({
                "key": "Description",
                "value": "This block Removes Null columns"
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "RemoveNullColumns"
            })
            block["Attributes"].append({
                "key": "Columns",
                "value": "All"
            })
        elif selection == "RemoveNullSelectedColumns":
            block["Attributes"].append({
                "key": "Description",
                "value": "This block Removes Null columns"
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "RemoveNullRows"
            })
            columns = self.SelectCols(self.dataName, params)
            block["Attributes"].append({
                "key": "Columns",
                "value": columns
            })
        elif selection == "ReplaceNullValues":
            block["Attributes"].append({
                "key": "Description",
                "value": "This block Replaces Null columns"
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "ReplaceNullValues"
            })
            block["Attributes"].append({
                "key": "Columns",
                "value": "All"
            })
            block["Attributes"].append({
                "key": "ReplaceWith",
                "value": params["replaceoptions"]
            })
        elif selection == "ReplaceSelectedNullValues":
            block["Attributes"].append({
                "key": "Description",
                "value": "This block Replaces Null columns"
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "ReplaceNullValues"
            })
            block["Attributes"].append({
                "key": "ReplaceWith",
                "value": params["replaceoptions"]
            })
            columns = self.SelectCols(self.dataName, params)
            block["Attributes"].append({
                "key": "Columns",
                "value": columns
            })
        elif selection == "RemoveOutliers":
            block["Attributes"].append({
                "key": "Description",
                "value": "This block Removes outlier values"
            })
            block["Attributes"].append({
                "key": "Apply",
                "value": "RemoveOutliers"
            })
            block["Attributes"].append({
                "key": "Option",
                "value": params["OutliersOptions"]
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

        self.deleteMLBlockifExist()
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

    def deleteMLBlockifExist(self):
        blocks = self.model["Blocks"]
        for index, block in enumerate(blocks):
            if block["Category"] == "Model":
                del blocks[index]
        self.model["Blocks"] = blocks

    def isBlockExist(self, selection, option=None):
        if selection == "ApplyStandardization" or selection == "ApplySelectedStandardization":
            for block in self.model["Blocks"]:
                if block["Category"] == "Transform":
                    attributes = processComplexJson(block["Attributes"])
                    if attributes["Apply"] == "Standardization":
                        return block
        elif selection == "ApplyNormalization":
            for block in self.model["Blocks"]:
                if block["Category"] == "Transform":
                    attributes = processComplexJson(block["Attributes"])
                    if attributes["Apply"] == "Normalization":
                        return block
        elif selection == "ApplySplitTrainTest":
            for block in self.model["Blocks"]:
                if block["Category"] == "Transform":
                    attributes = processComplexJson(block["Attributes"])
                    if attributes["Apply"] == "SplitTrainTest":
                        return block
        elif selection == "RemoveNullRows" or selection == "RemoveNullSelectedColumns":
            for block in self.model["Blocks"]:
                if block["Category"] == "Transform":
                    attributes = processComplexJson(block["Attributes"])
                    if attributes["Apply"] == "RemoveNullRows":
                        return block
        elif selection == "ReplaceNullValues" or selection == "ReplaceSelectedNullValues":
            for block in self.model["Blocks"]:
                if block["Category"] == "Transform":
                    attributes = processComplexJson(block["Attributes"])
                    if attributes["Apply"] == "ReplaceNullValues":
                        return block
        elif selection == "RemoveOutliers":
            for block in self.model["Blocks"]:
                if block["Category"] == "Transform":
                    attributes = processComplexJson(block["Attributes"])
                    if attributes["Apply"] == "RemoveOutliers":
                        return block
        return None

    def ModifyTheExistingBlock(self, block, columns, option=None, params=None):
        attributes = processComplexJson(block["Attributes"])
        if option != None:
            for index, att in enumerate(block["Attributes"]):
                if (att["key"] == "Option"):
                    block["Attributes"][index]["value"] = option
            return [block, ""]
        elif "ReplaceWith" in attributes:
            for index, att in enumerate(block["Attributes"]):
                if (att["key"] == "ReplaceWith"):
                    block["Attributes"][index]["value"] = params["replaceoptions"]
            return [block, ""]
        elif "Columns" in attributes:
            if attributes["Columns"] == "All":
                return [block, "Applied to all columns already, Remove the block first."]
            elif columns == "All":
                for index, att in enumerate(block["Attributes"]):
                    if (att["key"] == "Columns"):
                        for col in columns:
                            block["Attributes"][index]["value"] = "All"
                return [block, ""]
            elif len(attributes["Columns"]) > 0:
                for index, att in enumerate(block["Attributes"]):
                    if (att["key"] == "Columns"):
                        for col in columns:
                            block["Attributes"][index]["value"].append(col)
                return [block, ""]

        else:
            return [block, "Something wrong"]

    def SelectCols(self, dataName, params):
        if dataName == "Iris":
            return params["columnsiris"]
        elif dataName == "Sales":
            return params["columnssales"]
        else:
            pass
        return []
