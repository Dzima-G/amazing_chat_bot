import vk_api
from vk_api.exceptions import ApiError
from vk_api.longpoll import VkEventType, VkLongPoll

from dialog_flow_api import detect_intent_response


def run_vk_bot(vk_token, project_id, language_code):
    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                response = detect_intent_response(
                    project_id,
                    event.user_id,
                    event.text,
                    language_code
                )

                if not response.query_result.intent.is_fallback:
                    answer = response.query_result.fulfillment_text

                    try:
                        vk.messages.send(
                            user_id=event.user_id,
                            message=answer,
                            random_id=0
                        )
                    except ApiError:
                        continue
