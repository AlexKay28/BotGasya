import os
import time
import numpy as np
from pprint import pprint
from dotenv import load_dotenv
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from src.answer import handle_default_message, play_game
from src.smart_gpt import answer_gasya_gpt

# Loading environmental variables
load_dotenv(".env")

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BOT_GROUP_ID = int(os.getenv("BOT_GROUP_ID"))


def get_chat_users_names(users):
    return [user["screen_name"] for user in users["profiles"] if "screen_name" in user]


def main():
    """
    Bot gasya scripts
    """
    vk_session = VkApi(token=ACCESS_TOKEN)
    session_api = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, BOT_GROUP_ID, wait=100)

    CHATS_CACHE = {}
    chat_history_ids = None
    attention_list = ["@botgasya", "гася", "гась", "гусман", "попугай", "бот"]
    stop_list = ["заткн", "завали", "молчи", "тихо", "вырубись", "подожд"]
    attention_iterations = 0

    print("Ok. Im a bot and Im ready to kek!)")
    for event in longpoll.listen():
        print(event)
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_user:
                user_id = event.message.from_id
                message = event.message.text.lower()
                bot_answer = handle_default_message(message)
                vk_session.method(
                    "messages.send",
                    {"user_id": user_id, "message": bot_answer, "random_id": 0},
                )
            elif event.from_chat:
                peer_id = event.message.peer_id
                message = event.message.text.lower()

                if "@botgasya" not in message and np.random.random() < 0.01:
                    m1, m2 = play_game(message)
                    dict_to_send = {"peer_id": peer_id, "message": m1, "random_id": 0}
                    vk_session.method("messages.send", dict_to_send)
                    dict_to_send = {"peer_id": peer_id, "message": m2, "random_id": 0}
                    vk_session.method("messages.send", dict_to_send)

                elif any([f in message for f in stop_list]):
                    attention_iterations = 0
                    dict_to_send = {"peer_id": peer_id, "message": "ok", "random_id": 0}
                    vk_session.method("messages.send", dict_to_send)

                elif attention_iterations > 0 or any(
                    [f in message for f in attention_list]
                ):
                    message = " ".join(message.split()[1:])
                    attention_iterations = (
                        10 if attention_iterations == 0 else attention_iterations
                    )

                    print("GPT answer")
                    bot_answer, chat_history_ids = answer_gasya_gpt(
                        message, chat_history_ids
                    )
                    dict_to_send = {
                        "peer_id": peer_id,
                        "message": bot_answer,
                        "random_id": 0,
                    }
                    vk_session.method("messages.send", dict_to_send)

                # elif "@botgasya" in message:
                #     chat_members = get_chat_users_names(
                #         vk_session.method(
                #             "messages.getConversationMembers", {"peer_id": peer_id}
                #         )
                #     )
                #     ans = handle_default_message(message, chat_members)
                #     dict_to_send = {"peer_id": peer_id, "message": ans, "random_id": 0}
                #     vk_session.method("messages.send", dict_to_send)

                elif event.message.text != "" and len(event.message.text) > 3:
                    if peer_id not in CHATS_CACHE.keys():
                        CHATS_CACHE[peer_id] = {"messages": [event.message.text]}
                    else:
                        CHATS_CACHE[peer_id]["messages"].append(event.message.text)
                    print(CHATS_CACHE)

                    if (
                        np.random.random() < 0.2
                        and len(CHATS_CACHE[peer_id]["messages"]) > 5
                    ):
                        ans = np.random.choice(CHATS_CACHE[peer_id]["messages"])
                        dict_to_send = {
                            "peer_id": peer_id,
                            "message": ans,
                            "random_id": 0,
                        }
                        vk_session.method("messages.send", dict_to_send)
                    # else:
                    #     print("GPT answer")
                    #     bot_answer, chat_history_ids = answer_gasya_gpt(
                    #         message, chat_history_ids
                    #     )
                    #     dict_to_send = {
                    #         "peer_id": peer_id,
                    #         "message": bot_answer,
                    #         "random_id": 0,
                    #     }
                    #     vk_session.method("messages.send", dict_to_send)


if __name__ == "__main__":
    while 1:
        try:
            main()
        except Exception as e:
            time.sleep(1)
            print(f"Exception [{e}] has occurred. Restart")
