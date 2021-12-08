import re
import pandas as pd
import numpy as np

BAD_WORDS = [
    "еблинтус",
    "чуча",
    "чепуха",
    "лох",
    "победитель шоу голос",
    "предендент на глав-пидора",
    "член банды балласов",
    "дрянь",
    "вонючка",
    "залупа рыжая",
    "жук бродвейный",
    "несквик",
    "алладин",
    "бормолей",
]


def get_default_answer(text: str):
    return np.random.choice(
        [
            f'Че ты доебался со своим "{text}", я смотрю аниме, отвечу позже...',
            f"ты серьезно это сейчас пишешь?",
            f"нет слов...",
            f"Что еще скажешь?",
            f"Отлично сказано! Класс!",
            f"Мб тебе лучше обратиться к @witlless",
            f"самое глупое что я слышал...",
            f"Ебать меня в жопу",
            f"А раньше ты так не базарил, казачок",
            f"Разрывная",
            f"Кек. хех",
            f"Слабое звено заговорило, дальше...",
            f"-_-",
            f"Чертовски смешно, ага",
            f"что",
            f"да, и что?",
            f"псих",
            f"xD",
            f"xД",
            f"лан я пошел",
            f"не знаю что сказать. мб ко мне в баню? в шестой",
            f"я не занимаю бабки",
            f"я тебя рофлю",
            f"у тебя подгорает?",
        ]
    )


def play_game(text: str):
    if np.random.random() > 0.1:
        anecdotes = pd.read_csv("data/anecdotes.csv")
        m1 = np.random.choice(
            [
                "Я если что тоже тут, мужики) Юморнем?",
                "Есть у меня тут прикол такой",
                "Недавно мне пришло письмо из горсовета, а там вот что было написано",
                "Зацените)))))))",
            ]
        )
        m2 = anecdotes.sample(1).text.to_list()[0].strip()
    else:
        m1 = "Я смотрю вы тут общаетесь) \nА ну ка тогда попробуем!"
        m2 = "@botv_pidor старт"
    return m1, m2


def handle_default_message(text: str, chat_members="Ты"):
    """
    Handle user message
    """
    if "наедь на дуру" in text:
        text = f"@witlless {np.random.choice(BAD_WORDS)}"
    elif "" == text:
        text = f"что"
    elif "не понял" in text:
        text = f"че ты не понял"
    elif any([f in text for f in ["себя", "гаси", "гасю", "себе", "гасе"]]):
        text = f"@sogekingg, ты {np.random.choice(BAD_WORDS)}"
    elif "молодец" in text:
        text = f"Спасибо, мужик!"
    elif any([f in text for f in ["назови", "кому", "кого"]]):
        text = f"Я думаю @{np.random.choice(chat_members)}. "
    elif any([f in text for f in ["иди", "пошел", "сходи"]]):
        text = f"Сам иди..."
    elif "ты" in text:
        text = np.random.choice(
            [
                f"нц... >_<",
                "xD",
                ")))))",
                f"не твой уровень, {np.random.choice(BAD_WORDS)}",
                f"а ну ка повтори, {np.random.choice(BAD_WORDS)}",
            ]
        )
    else:
        text = re.sub("\[.*\]", "", text).strip()
        text = get_default_answer(text)
    return text
