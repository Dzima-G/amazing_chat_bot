import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    try:
        response = intents_client.create_intent(
            request={"parent": parent, "intent": intent}
        )

        print("Intent created: {}".format(response))
    except Exception as e:
        print(f"Ошибка при создании intent '{display_name}': {e}")


if __name__ == '__main__':

    load_dotenv()
    project_id = os.environ['PROJECT_GOOGLE_CLOUD_ID']

    with open('intent/intents.json', 'r', encoding='utf-8') as my_file:
        intents_data = json.load(my_file)

    for display_name, item in intents_data.items():
        training_phrases_parts = item.get('questions', [])
        message_texts = [item.get('answer', '')]

        create_intent(
            project_id,
            display_name,
            training_phrases_parts,
            message_texts,
        )
