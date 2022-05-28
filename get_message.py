import urllib3
import botik
import requests
from json import loads
from random import choice, randint
from time import sleep
from multiprocessing import Pool
import re
urllib3.disable_warnings()

print("Bot by Tëma | Crypto Hub x 1enechka ")
discordToken = input('Введите токен от аккаунта: ')
chatid = input('Введите id чата: ')
pause = int(input('Введите кулдаун между сообщениями: '))
lang = input('На каком языке чат (rus/eng): ')
iiProb = int(input('Вероятность ответа ИИ (0-100): '))
distanceBetweenMessages = int(input('Какое расстояние выдерживать между сообщениями (количество сообщений, не должно быть меньше 10): '))
numOfMessages = int(input('Количество сообщений (введите 0, чтобы пропустить): '))
if (numOfMessages!=0):
    freqOfNotif = int(input('Частота вывода количества сообщений: '))
typing_sleep = int(input('Введите время имитирования печатания сообщения: '))
message = ""
dictMain = {}
arrKeys = []
aurhors = []
messagelist = []
discordtokens = []

with open('message.txt', encoding="utf8") as msg:
    lines = msg.readlines()
    for line in lines:
        messagelist.append(line)

session = requests.Session()
session.headers['authorization'] = discordToken

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
    r = session.get(f'https://discord.com/api/v9/channels/{chatid}/messages?limit=12')
    try:
        username = loads(session.get('https://discordapp.com/api/users/@me', verify=False).text)['username']
    except:
        print(f'Не смог получить имя аккаунта с токеном: {discordtoken}')
    for i in range(10):
        ids = loads(r.text)[i]['id']
        message = loads(r.text)[i]['content']
        author = loads(r.text)[i]['author']
        aurhors.append(author)
        dictMain[ids] = message
        arrKeys.append(ids)

    print(arrKeys)

    num = randint(0, 9)

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


def distanceChecker():
    checkPointID = ""

    # chatid = '934435591230226475'
    # discordtoken = 'OTUzOTcwNjkyMTg4MTUxODE5.Yjx4HA.BI1BRG78DaxuaR72FRBRaBBn1bA'

    session = requests.Session()
    session.headers['authorization'] = discordToken

    r = session.get(f'https://discord.com/api/v9/channels/{chatid}/messages?limit={distanceBetweenMessages}')
    try:
        username = loads(session.get('https://discordapp.com/api/users/@me', verify=False).text)['username']
    except:
        print(f'Не смог получить имя аккаунта с токеном: {discordToken}')
    for i in range (distanceBetweenMessages):
        ids = loads(r.text)[i]['id']
        arrKeys.append(ids)

    checkPointID = arrKeys[0]
        
    while (checkPointID in arrKeys):
        arrKeys.clear()
        r = session.get(f'https://discord.com/api/v9/channels/{chatid}/messages?limit={distanceBetweenMessages}')
        for i in range (distanceBetweenMessages):
            ids = loads(r.text)[i]['id']
            arrKeys.append(ids)
        sleep(15)



def main(discordtoken):
    if (numOfMessages==0):
        tmp=0
        while (True):
            try:
                x = randint(1, 100)
                if x <= iiProb:
                    random_message_sent(discordtoken)
                else:
                    BotAnswer(discordtoken)
                tmp+=1
                print(f'\033[1;31m ######### Отправленно {tmp} сообщений #########\033[0;0m')
                distanceChecker()
            except Exception as ex:
                print(ex)
    else:
        for i in range(1, numOfMessages):
            try:
                x = randint(1, 100)
                if x <= iiProb:
                    random_message_sent(discordtoken)
                else:
                    BotAnswer(discordtoken)
                if (i%freqOfNotif==0):
                    print(f'\033[1;31m ######### Отправленно {i} сообщений #########\033[0;0m')
                distanceChecker()
            except Exception as ex:
                print(ex)


if __name__=='__main__':
    main(discordToken)