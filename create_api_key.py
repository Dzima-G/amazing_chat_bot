import argparse
import os

from dotenv import load_dotenv
from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key


def create_api_key(project_id: str, suffix: str) -> Key:
    """
    Creates and restrict an API key. Add the suffix for uniqueness.

    TODO(Developer):
    1. Before running this sample,
      set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    2. Make sure you have the necessary permission to create API keys.

    Args:
        project_id: Google Cloud project id.

    Returns:
        response: Returns the created API Key.
    """
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f"API key - {suffix}"

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f"projects/{project_id}/locations/global"
    request.key = key

    response = client.create_key(request=request).result()

    return response


if __name__ == '__main__':
    load_dotenv()
    project_id = os.environ['PROJECT_GOOGLE_CLOUD_ID']
    env_suffix = os.getenv('SUFFIX', None)

    suffix_parser = argparse.ArgumentParser(
        description='Введите суффикс к названию ключа (например: amazing-chat-bot).'
    )
    suffix_parser.add_argument(
        'suffix',
        type=str,
        nargs='?',
        default=None,
        help='Суффикс к названию ключа'
    )

    args = suffix_parser.parse_args()

    if args.suffix is not None:
        suffix = args.suffix
    elif env_suffix is not None:
        suffix = env_suffix
    else:
        suffix = 'amazing-chat-bot'

    response = create_api_key(project_id, suffix)
    print(f"Успешно создан API key: {response.name}")
