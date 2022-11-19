from google.cloud import dialogflow_v2beta1 as dialogflow
from google.oauth2 import service_account
import json


dialogflow_key = json.load(open('key2.json'))
credentials = (
    service_account.Credentials.from_service_account_info(dialogflow_key))
DIALOGFLOW_PROJECT_ID = 'proj-slate-rekj'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_APPLICATION_CREDENTIALS = 'key.json'
SESSION_ID = 'test-client'


def detect_intent(text):
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    text_input = dialogflow.TextInput(
        text=text, language_code=DIALOGFLOW_LANGUAGE_CODE)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input})

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print("Fulfillment text: {}\n".format(
        response.query_result.fulfillment_text))

    return json.loads(response.query_result.fulfillment_text)
