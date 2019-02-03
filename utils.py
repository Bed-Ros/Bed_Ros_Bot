# coding=utf-8

import config
import urllib2
import json
import pandas
from time import sleep

# Сообщение в чат
def mess(sock, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(config.CHAN, message))


# Заполнение словаря чата
def fillchatlist():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/melharucos/chatters"
            req = urllib2.Request(url, headers={"accept": "*/*"})
            res = urllib2.urlopen(req).read()
            if res.find("502 bad gateway") == - 1:
                config.chatlist.clear()
                data = json.loads(res)
                for p in data["chatters"]["moderators"]:
                    config.chatlist[p] = "mod"
                for p in data["chatters"]["global_mods"]:
                    config.chatlist[p] = "global_mod"
                for p in data["chatters"]["admins"]:
                    config.chatlist[p] = "admin"
                for p in data["chatters"]["staff"]:
                    config.chatlist[p] = "staff"
                for p in data["chatters"]["viewers"]:
                    config.chatlist[p] = "viewer"
        except:
            "Something went wrong...do nothing"
        sleep(5)

# Это модератор?
def isMod(user):
    if user in config.chatlist.keys():
        if config.chatlist[user] == "mod":
            return True
        else:
            return False

#Заполнение словаря баллов
def fillpointlist():

    sleep(5)

    while True:
        # Начисление баллов за просмотр стрима
        for p in config.chatlist.keys():
            if p in config.df.index:
                if config.df.loc[p, 'Points'] < 2000000:
                    if config.df.loc[p, 'Points'] == '':
                        config.df.loc[p, 'Points'] = 1
                    else:
                        config.df.loc[p, 'Points'] += 1
            else:
                config.df.loc[p] = [p, 1, '']
        # Сортировка
                config.df = config.df.sort_values(by=['Points'], ascending=[False])
        # Запись вспомогательного файла в основной
        writer = pandas.ExcelWriter('points.xlsx')
        config.df.to_excel(writer, sheet_name='Board', columns=['Points', 'Games'], index=True)
        writer.save()

        sleep(5)