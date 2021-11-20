import os
from pprint import pprint
from dotenv import load_dotenv
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from src.answer import handle_message

# Loading environmental variables
# load_dotenv(".env")

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

vk_session = VkApi(token=ACCESS_TOKEN)
session_api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)


def main():
    print("Go!")
    for event in longpoll.listen():
        print("\n\n")
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            if event.from_user:
                user_id = event.message.from_id
                message = event.message.text.lower()

                bot_answer = handle_message(message)

                vk_session.method(
                    "messages.send",
                    {"user_id": user_id, "message": bot_answer, "random_id": 0},
                )
            else:
                peer_id = event.message.peer_id
                message = event.message.text.lower()

                bot_answer = handle_message(message)

                vk_session.method(
                    "messages.send",
                    {"peer_id": peer_id, "message": bot_answer, "random_id": 0},
                )


if __name__ == "__main__":
    main()
