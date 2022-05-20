import urllib3
import botik
import requests
from json import loads
from random import choice, randint
from time import sleep
from multiprocessing import Pool
import re
urllib3.disable_warnings()

print("Bot by Tëma | Crypto Hub x Flexter")
#discordtoken = input('Введите токен от аккаунта: ')
chatid = input('Введите id чата: ')
pause = int(input('Введите кулдаун в чате в секундах: '))
lang = input('На каком языке чат (rus/eng): ')
typing_sleep=int(input('Введите время имитирования печатания сообщения: '))
account_counts = int(len(re.findall(r"[\n']+", open('tokens.txt').read())))
message = ""
dictMain = {}
arrKeys = []
aurhors = []
messagelist = []
discordtokens =[]
with open('message.txt',encoding="utf8") as msg:
    lines = msg.readlines()
    for line in lines:
        messagelist.append(line)


with open('tokens.txt', encoding='utf8') as tokens:
    token = tokens.readlines()
    for discordtoken in token:
        discordtokens.append(discordtoken.rstrip())

session = requests.Session()
session.headers['authorization'] = discordtoken

r = session.get(f'https://discord.com/api/v9/channels/{chatid}/messages?limit=1')
#lastid = loads(r.text)[0]['id']

r = session.get(f'https://discord.com/api/v9/channels/{chatid}/messages?limit=12')
def random_message_sent(discordtoken):
    session = requests.Session()
    session.headers['authorization'] = discordtoken
    try:
        username = loads(session.get('https://discordapp.com/api/users/@me', verify=False).text)['username']
    except:
        print(f'Не смог получить имя аккаунта с токеном: {discordtoken}')
    r = session.post(f'https://discord.com/api/v9/channels/{chatid}/typing', verify=False)
    sleep(typing_sleep)
    randommessage = choice(messagelist)
    data = {'content': randommessage, 'tts': False}
    session.post(f'https://discord.com/api/v9/channels/{chatid}/messages', json=data, verify=False)
    if username:
        print(f'Successfully sent random message [{randommessage}] without reply on the account with name [{username}].')
    sleep(pause)


def BotAnswer(discordtoken):
    session = requests.Session()
    session.headers['authorization'] = discordtoken
    try:
        username = loads(session.get('https://discordapp.com/api/users/@me', verify=False).text)['username']
    except:
        print(f'Не смог получить имя аккаунта с токеном: {discordtoken}')
    for i in range (10):
        ids = loads(r.text)[i]['id']
        message = loads(r.text)[i]['content']
        author = loads(r.text)[i]['author']
        aurhors.append(author)
        dictMain[ids] = message
        arrKeys.append(ids)

    num = randint(0,9)

    if lang == "rus":
        otvet = str(botik.rus_bot_rand(dictMain[arrKeys[num]]))
    if lang == "eng":
        otvet = str(botik.eng_bot_rand(dictMain[arrKeys[num]]))

    data_for_first_answer = {'content': otvet, 'message_reference':
                        {
                            "message_id": arrKeys[num]
                        },
                            'tts': False}
    session.post(f'https://discord.com/api/v9/channels/{chatid}/typing', verify=False)
    sleep(typing_sleep)
    session.post(f'https://discord.com/api/v9/channels/{chatid}/messages', json=data_for_first_answer, verify=False)
    print (f'Successfully send message [{otvet}] on the account with name [{username}]')
    sleep(pause)

def main(discordtoken):
    while True:
        try:
            x = randint(1, 10)
            if x <= 7:
                random_message_sent(discordtoken)
            else:
                BotAnswer(discordtoken)
        except Exception as ex:
            print(ex)

# while (1):
#     try:
#         BotAnswer()
#         sleep(pause)
#         x = randint(1, 3)
#         if x ==2:
#             random_message_sent(discordtoken)
#             sleep(pause)
#     except Exception as ex:
#         print(ex)

if __name__=='__main__':
    p = Pool(processes=account_counts+1)
    p.map(main, discordtokens)