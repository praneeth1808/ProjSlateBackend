from flask import Flask, request, jsonify
from detectIntent import detect_intent
from JsonModel.jsonModel import JsonModel as JM


app = Flask(__name__)

jsonModel = JM()
print(jsonModel.resetModel())
print(jsonModel.saveModel())

@app.route('/process/', methods=['GET'])
def respond():
    # input the string as text
    text = request.args.get("text", None)
    print(f"Received: {text}")

    response = {

     }
    
    if not text:
        response["ERROR"] = "No text Found found. Please send a text."
    else:
        response = {
        "ActionItem": detect_intent(text)
     }

    # Return the response in json format
    return jsonify(response)

@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to Project Slate</h1>"









if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
