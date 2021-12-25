import pyrogram
from pyrogram import Client, idle, filters
from pyrogram.handlers import MessageHandler
from time import sleep
from os import system
from configparser import ConfigParser

config = ConfigParser()

try:
    with open('config.ini', 'r') as f:
        config.read('config.ini')
except:
    with open('config.ini', 'w') as f:
        config.add_section('main')
        config.set('main', 'api_id', 'value0')
        config.set('main', 'api_hash', 'value1')
        config.set('main', 'channel_id', 'value2')
        config.set('main', 'msg_txt', 'value3')
        config.set('main', 'delay_msg', 'value4')
        config.set('main', 'numbers', 'value5')
        config.set('main', 'count_users_send', 'value6')
        config.set('main', 'log', 'value7')
        config.write(f)
        print('Заполните settings.ini')
        exit()

old_ids = []
ids = []
metion = []
my_apps = []
settings = {'channel_id': 'gg', 'delay_msg': 10, 'count_users_send': 20, 'msg_txt': "Всем привет!","numbers": "+7900000000, +7900000100", "log": 0}


api_id = config.get('main', 'api_id').split(', ')
api_hash = config.get('main', 'api_hash').split(', ')
channel_id = config.get('main', 'channel_id').split(', ')
msg_txt = config.get('main', 'msg_txt')
delay_msg = config.get('main', 'delay_msg')
numbers = config.get('main', 'numbers').split(', ')
log = config.get('main', 'log')
count_users_send = config.get('main', 'count_users_send')

for i in range(0, len(numbers)):
    my_apps.append(Client(f"app{i}"))
    
    with Client(f"app{numbers[i]}", int(api_id[i]), api_hash[i]) as my_apps[i]:
        pass

def log_txt(m):
    if int(log) == 1:
        print(m)

def get_online_members():
    with Client(f"app{numbers[0]}", api_id[0], api_hash[0]) as my_apps[0]:
        app1 = my_apps[0]
        for k in channel_id:
            log_txt('получаем участников...')
            users = app1.iter_chat_members(k)
            for i in range(0,len(users)):
                if users[i]['user']['status'] == "online":
                    ids.append(str(users[i]['user']['id']))
    for i in range(1, len(my_apps)):
        with Client(f"app{numbers[i]}", api_id[i], api_hash[i]) as my_apps[i]:
            my_apps[i].iter_chat_members(k)
 
def smsSpam(app):
    old_s = ''
    s = ''
    count = 0
    for g in old_ids:
        try:
            ids.remove(g)
        except:
            pass
    while True:
        for v in ids:
            s = v
            del ids[:1]
            
            if old_s != s:
                if count != int(count_users_send):
                    try:
                        app.send_message(int(s), msg_txt, parse_mode="markdown")
                        count += 1
                    except pyrogram.errors.exceptions.bad_request_400.PeerFlood:
                        print('На этом аккаунте лимит сообщений')
                        break
                    except pyrogram.errors.exceptions.bad_request_400.PeerIdInvalid:
                        print('IdInvalid 400')
                else:
                    print(f'Пользователи подошли к концу: {int(count_users_send)}')
                    break
            else:
                print('Все сделанно!')
                break
            
            old_s = s
            
            log_txt(f"left: {len(ids)}")
            log_txt(f"user_send: {s}")
            sleep(float(delay_msg))
        else:
            continue
        break


if __name__ == "__main__":
    get_online_members()
    for i in range(0, len(my_apps)):
        with Client(f"app{numbers[i]}", int(api_id[i]), api_hash[i]) as my_apps[i]:
            print(f'App - {my_apps[i]}')
            smsSpam(my_apps[i])