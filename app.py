from flask import Flask, request, jsonify
from detectIntent import detect_intent
from JsonModel.jsonModel import JsonModel as JM
from ProcessModel.model import Model

app = Flask(__name__)

model = Model()


@app.route('/process/', methods=['GET'])
def respond():
    # input the string as text
    text = request.args.get("text", None)
    print(f"Received: {text}")

    response = {}

    if not text:
        response["ERROR"] = "No text Found found. Please send a text."
    else:
        response = model.process(text)

    # Return the response in json format
    return jsonify(response)


@app.route('/results/', methods=['GET'])
def respond_res():
    return jsonify(model.Results())


@app.route('/getModel/', methods=['GET'])
def respond_get():
    return jsonify(model.getModel())


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to Project Slate</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
