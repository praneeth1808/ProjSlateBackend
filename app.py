from flask import Flask, request, jsonify
from detectIntent import detect_intent
from JsonModel.jsonModel import JsonModel as JM
from ProcessModel.model import Model
from flask_cors import CORS, cross_origin

# Run command : nodemon --ignore 'data/' --exec python3 app.py


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model = Model()


@app.route('/process/', methods=['GET'])
def respond():
    try:
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
    except Exception as err:
        return jsonify({"messageType": "Error", "message": str(err), "model": model.getModel(), "Results": {},
                        "CurrentProcess": {}, "Scores": {}, "Graphs": {}})


@app.route('/results/', methods=['GET'])
def respond_res():
    return jsonify(model.Results())


@app.route('/resetModel/', methods=['GET'])
def respond_reset():
    model.ResetModel()
    return jsonify({"messageType": "", "message": "", "CurrentProcess": {}, "Results": None, "model": model.ResetModel()})


@app.route('/get/', methods=['GET'])
def respond_get():
    return jsonify(model.returnRes(None))


@app.route('/scores/', methods=['GET'])
def respond_getscores():
    return jsonify({"Scores": model.scores})


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to Project Slate</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
