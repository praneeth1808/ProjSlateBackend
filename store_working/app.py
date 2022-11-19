from flask import Flask, request, jsonify
from google.cloud import dialogflow_v2beta1 as dialogflow
from google.oauth2 import service_account
import json
app = Flask(__name__)

dialogflow_key = json.load(open('key2.json'))
credentials = (service_account.Credentials.from_service_account_info(dialogflow_key))
DIALOGFLOW_PROJECT_ID = 'proj-slate-rekj'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_APPLICATION_CREDENTIALS = 'key.json'
SESSION_ID = 'test-client'


@app.route('/message/', methods=['GET'])
def respond():
    # Retrieve the name from the url parameter /getmsg/?name=
    text = request.args.get("text", None)

    # For debugging
    print(f"Received: {text}")

    response = {}
    print(detect_intent_texts(DIALOGFLOW_PROJECT_ID, SESSION_ID, [text], DIALOGFLOW_LANGUAGE_CODE))
    # Check if the user sent a name at all
    if not text:
        response["ERROR"] = "No messageFound found. Please send a name."
    else:
        response["MESSAGE"] = f"We are processing your message: {text}"

    # Return the response in json format
    return jsonify(response)


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome API!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "No name found. Please send a name."
        })


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome to our medium-greeting-api!</h1>"


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient(credentials=credentials)

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))









if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
