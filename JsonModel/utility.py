import json
import os

def getDataFilePath(filename):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
    return os.path.join(ROOT_DIR,"..","data",filename)

def readJson(filename):
    filePath = getDataFilePath(filename)
    f = open(filePath)
    data = json.load(f)
    return data


def writeJson(filename,data):
    filePath = getDataFilePath(filename)
    json_object = json.dumps(data)
    with open(filePath, "w") as outfile:
        outfile.write(json_object)
    return True


