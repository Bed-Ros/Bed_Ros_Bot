# coding=utf-8

import pandas

# Основные константы
HOST = "irc.twitch.tv"
PORT = 6667
NICK = "Bed_Ros_Bot"
PASS = "oauth:vwdmxiugq7nh4a3olb6tql46h4f00q"
CHAN = "bed_ros"

# Ссылка на таблицу в облаке
file_link = 'https://drive.google.com/file/d/1KQqvGXmnleIkfINSapvalqdIkZIlgDHQ/view?usp=sharing'

# Словарь текущих людей в чате
# ник - должность
chatlist = {}

# Таблица очков и игр
xl = pandas.ExcelFile('points.xlsx')
df = xl.parse("Board")
df.index = df.Nicks
