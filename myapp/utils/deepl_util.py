import os

import deepl
from dotenv import load_dotenv

load_dotenv()

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
if not DEEPL_API_KEY:
    raise EnvironmentError("DEEPL_API_KEYが設定されていません。")


def translate(text, target):
    auth_key = DEEPL_API_KEY
    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang=target)
    return result.text
