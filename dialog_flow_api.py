from google.api_core.exceptions import GoogleAPICallError, RetryError
from google.cloud import dialogflow


def detect_intent_response(project_id: str, session_id: str, text: str, language_code: str):
    """Returns the result of detect intent with texts as inputs.

        Using the same `session_id` between requests allows continuation
        of the conversation."""
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)

        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={
                "session": session,
                "query_input": query_input}
        )
        return response

    except (GoogleAPICallError, RetryError) as e:
        return 'Я временно не могу отвечать, прошу прощения.'
