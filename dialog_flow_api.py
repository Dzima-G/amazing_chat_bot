from google.api_core.exceptions import GoogleAPICallError, RetryError
from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id, text, language_code):
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)

        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={
                "session": session,
                "query_input": query_input
            }
        )

        return response.query_result.fulfillment_text

    except (GoogleAPICallError, RetryError) as e:
        return 'Я временно не могу отвечать, прошу прощения.'


def detect_intent_response(project_id, session_id, text, language_code):
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)

        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        return response

    except (GoogleAPICallError, RetryError) as e:
        return 'Я временно не могу отвечать, прошу прощения.'