import requests
from translatepy.translators.google import GoogleTranslate



def rus_bot_rand(text):
    quest = text
    r = requests.post("https://xu.su/api/send", data={'uid':"c7b245c0-1016-4ff2-82b4-cdcce8eb4b28", 'bot': "Ваня-Петух", "text": quest})
    answer = str(r.json())
    answer = answer[:answer.find("', 'u")]
    answer = answer[22:]
    return answer

def eng_bot_rand(text):
    gtranslate = GoogleTranslate()
    trans = gtranslate.translate(text=text, source_language='en', destination_language='ru')
    quest = trans
    r = requests.post("https://xu.su/api/send",data={'uid':"c7b245c0-1016-4ff2-82b4-cdcce8eb4b28", 'bot': "Ваня-Петух", "text": quest})
    answer = str(r.json())
    answer = answer[:answer.find("', 'u")]
    answer = answer[22:]
    end = gtranslate.translate(text=answer, source_language='ru', destination_language='en')
    return end