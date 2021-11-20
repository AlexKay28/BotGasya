import re


def handle_message(text):
    """
    Handle user message
    """
    text = re.sub("\[.*\]", "", text).strip()
    text = f'Че ты доебался со своим "{text}", я смотрю аниме, отвечу позже...'
    return text
