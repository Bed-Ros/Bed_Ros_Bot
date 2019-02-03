# coding=utf-8

import random
import config
import utils
import socket
import re
import time
import thread
from time import sleep


def main():
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))

    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

    thread.start_new_thread(utils.fillchatlist, ())
    thread.start_new_thread(utils.fillpointlist, ())

    sleep(10)
    utils.mess(s, "Я вернулся. MrDestructoid")

    T = 0
    on = True
    while on:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("POND :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = chat_message.sub("", response)
            print(response)
            # Показывает баллы usernam'а
            if message.strip() == "!mypoints":
                if username in config.df.index:
                    utils.mess(s, '@' + str(username) + " твой счет " + str(config.df.loc[str(username), 'Points']))
                else:
                    utils.mess(s, "Таак'с посмотрим... сейчас поищу... @" + str(username) + " зайди через секунд 10")
            # Заказ игры
            if message.strip().startswith("!game "):
                config.df.loc[username, 'Games'] = message.replace("!game ", "").strip()
                utils.mess(s, '@' + str(username) + " Игра добавлена ;)")
            # Показ таблицы баллов
            if message.strip() == "!table":
                utils.mess(s, 'Актуальная таблица баллов и заказанных игр по ссылке: ' + config.file_link)
            # Показать сколько времени прошло с начала стрима
            if message.strip() == "!uptime":
                if T == 0:
                    utils.mess(s, "Стрим еще не начался")
                else:
                    a = time.time() - T
                    h = "{0:.0f}".format(a // 3600)
                    m = "{0:.0f}".format((a // 60) % 60)
                    sec = "{0:.0f}".format(a % 60)
                    utils.mess(s, "С начала стрима прошло " + str(h) + " ч " + str(m) + " м " + str(sec) + " c")
            # Пожать руку случайному человеку в чате
            if message.strip() == "!rnd":
                g = random.choice(config.chatlist.keys())
                while g == username:
                    g = random.choice(config.chatlist.keys())
                utils.mess(s, '@' + str(username) + " пожал руку @" + str(g))

            # Выбор следующей игры
            win = config.df.iloc[0]
            if message.strip() == "!winner" and username == config.CHAN:
                utils.mess(s, 'Выиграл @' + str(config.df.loc[win, 'Nicks']) + ' с ' + str(config.df.loc[win, 'Points']) + ' баллами и следующая игра это ' + str(config.df.loc[win, 'Games']))
            # Начало стрима
            if message.strip() == "!begin" and username == config.CHAN:
                if T != 0:
                    utils.mess(s, "Стрим еще не закончился")
                else:
                    T = time.time()
                    utils.mess(s, "Начало стрима!")
            # Конец стрима
            if message.strip() == "!end" and username == config.CHAN:
                if T == 0:
                    utils.mess(s, "Стрим еще не начался")
                else:
                    T = 0
                    utils.mess(s, "Конец стрима")
            # Завершение работы бота
            if message.strip() == "!offbot" and username == config.CHAN:
                on = False
        sleep(1)
    # При завершении работы бота
    utils.mess(s, "Я ушел. MrDestructoid")


if __name__ == "__main__":
    main()
