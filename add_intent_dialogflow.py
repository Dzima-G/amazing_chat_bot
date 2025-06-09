import argparse
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

        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    return f'Добавлен intent: {response.display_name}'


if __name__ == '__main__':

    load_dotenv()
    project_id = os.environ['PROJECT_GOOGLE_CLOUD_ID']
    env_local_path = os.getenv('LOCAL_PATH', None)

    parser_local_path = argparse.ArgumentParser(
        description='Введите путь к файлу c intent (намерения), например: intent/intents.json'
    )
    parser_local_path.add_argument(
        'local_path',
        type=str,
        nargs='?',
        default=None,
        help='Путь к файлу с intent'
    )

    args = parser_local_path.parse_args()

    if args.local_path is not None:
        local_path = args.local_path
    elif env_local_path is not None:
        local_path = env_local_path
    else:
        local_path = 'intent/intents.json'

    with open(local_path, 'r', encoding='utf-8') as data:
        intents_data = json.load(data)

    for display_name, item in intents_data.items():
        training_phrases_parts = item.get('questions', [])
        message_texts = [item.get('answer', '')]

        try:
            response = create_intent(
                project_id,
                display_name,
                training_phrases_parts,
                message_texts,
            )

            print(response)

        except Exception as e:
            print(f"Ошибка при создании intent '{display_name}': {e}")
