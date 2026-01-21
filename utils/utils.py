from deep_translator import GoogleTranslator

def translate_text(sourse, language):
    with open(f"{sourse}", "r", encoding="utf-8") as file:
        text = file.read()
    translate_text = GoogleTranslator(source='auto', target=language).translate(text)
    return translate_text