# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta
import time
import pytz

# Сегодняшняя дата, для добавления их в базу данных
time_is = str(datetime.now())
time_is = time_is[:10]

# Завтрашняя дата, для добавления в базу данных
previous_day = (str(datetime.now() + timedelta(days=1)))[:10]

# Кортеж всех URL сылок для парсиннга, каждый отдельный знак имеет свою уникальную ссылку
# День сегодняшний
end_of_url_today = {
    'Овен': '?znak=aries',  # aries
    'Телец': '?znak=taurus',  # taurus
    'Близнец': '?znak=gemini',  # gemini
    'Рак': '?znak=cancer',  # cancer
    'Лев': '?znak=leo',  # leo
    'Дева': '?znak=virgo',  # virgo
    'Весы': '?znak=libra',  # libra
    'Скорпион': '?znak=scorpio',  # scorpio
    'Стрелец': '?znak=sagittarius',  # sagittarius
    'Казерог': '?znak=capricorn',  # capricorn
    'Водолей': '?znak=aquarius',  # aquarius
    'Рыба': '?znak=pisces',  # pisces
}
# Кортеж всех URL сылок для парсиннга, каждый отдельный знак имеет свою уникальную ссылку
# День завтрашний
end_of_url_tomorrow = {
    'Овен': '?znak=aries&kn=tomorrow',  # aries
    'Телец': '?znak=taurus&kn=tomorrow',  # taurus
    'Близнец': '?znak=gemini&kn=tomorrow',  # gemini
    'Рак': '?znak=cancer&kn=tomorrow',  # cancer
    'Лев': '?znak=leo&kn=tomorrow',  # leo
    'Дева': '?znak=virgo&kn=tomorrow',  # virgo
    'Весы': '?znak=libra&kn=tomorrow',  # libra
    'Скорпион': '?znak=scorpio&kn=tomorrow',  # scorpio
    'Стрелец': '?znak=sagittarius&kn=tomorrow',  # sagittarius
    'Казерог': '?znak=capricorn&kn=tomorrow',  # capricorn
    'Водолей': '?znak=aquarius&kn=tomorrow',  # aquarius
    'Рыба': '?znak=pisces&kn=tomorrow',  # pisces
}
# Имя браузера, что бы сервер думал что это человек
head = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

# Функция для парсинга данных с сайта
def pars_and_clean(One, Two):
    convert = []
    # Данные сегоднящнего дня
    if One:
        for item in end_of_url_today.values():
            url = 'https://1001goroskop.ru/' + str(item)
            # Начинаем парсить данные с сайта
            full_page = requests.get(url, headers=head)
            soup = BeautifulSoup(full_page.content, 'html.parser')
            convert_data = soup.findAll('div', {'itemprop': 'description'})
            # Обрабатываем нужные нам данные
            convert.append([x.text for x in convert_data])
        return convert

    # Данные завтрашнего дня
    if Two:
        for item in end_of_url_tomorrow.values():
            url = 'https://1001goroskop.ru/' + str(item)
            # Начинаем парсить данные с сайта
            full_page = requests.get(url, headers=head)
            soup = BeautifulSoup(full_page.content, 'html.parser')
            convert_data = soup.findAll('div', {'itemprop': 'description'})
            # Обрабатываем нужные нам данные
            convert.append([x.text for x in convert_data])
        return convert

# Добавляем даты в список данных
def sett(today, tomorrow):
    clue = []
    finish = []
    # Данные сегодняшего дня
    for key in end_of_url_today.keys():
        clue.append(str(key))
    for number, index in enumerate(today, 0):
        index.insert(0, clue[number])
        index.append(time_is)
        finish.append(index)
    clues = []
    finish_t = []

    # Данные завтрашнего дня
    for key in end_of_url_tomorrow.keys():
        clues.append(str(key))
    for number, index in enumerate(tomorrow, 0):
        index.insert(0, clues[number])
        index.append(previous_day)
        finish_t.append(index)
    return finish, finish_t

# Функция для созданния соединения с SQLite3 базы данных
def create_connection(path):
    connect = None
    try:
        connect = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connect

# Добавляем свои данные в базу данных
def execute_query(connect):
    cursor = connect.cursor()
    try:
        for index in convert_today:
            cursor.execute(f'INSERT INTO users VALUES (?, ?, ?)', (index[0], index[1], index[2]))

        for index in convert_tomorrow:
            cursor.execute(f'INSERT INTO users VALUES (?, ?, ?)', (index[0], index[1], index[2]))
            connect.commit()
            print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Функция чтения данных из базы данных
def execute_read_query(connect, query):
    cursor = connect.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

# Удаление всей информации в базе данных
def del_query(connect):
    cursor = connect.cursor()
    try:
        cursor.execute(f'DELETE FROM users;')
        connect.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Вывод всей информации из базы данных
def look_for_hor():
    select_users = "SELECT * from users"
    users = execute_read_query(connection, select_users)
    for user in users:
        print(user)

# Бесконечный цикл для обновления данных в SQLite3
# Работает он следующим образов:
# Каждую минуту скрипт "Просыпается" и проверяет текущее время (по Мосвке) 
# Если в Москве время 12.01, то в это время сайт обновляет свои данные гороскопа
# Скрипт начинает обновлять данные в базе даннных, удаляя старые
startnew=1
while True:
    # Обновление на сайте происходит по московскому времени
    moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
    moscow_time = str(moscow_time)[11:15]+'0'
    print("moscow_time - " + moscow_time)
    # Если время по МСК 12.01 то скрипт начинает свою работу
    if moscow_time == "00:10" or startnew==1:
        startnew=0
        print('The download process is underway.')
        first, Sec = True, False
        convert_today = pars_and_clean(first, Sec)
        Sec, first = True, False
        convert_tomorrow = pars_and_clean(first, Sec)
        convert_today, convert_tomorrow = sett(convert_today, convert_tomorrow)\

        connection = create_connection("base_of_horoscope.sqlite")

        del_query(connection)  # Удаляем данные в бд
        execute_query(connection)  # Добавляем то, что спарсили
        look_for_hor()  # Вызываем, что бы проверить Гороскоп
        print("Is's finish.")
        # Отправляем скрип в "Сон"
        time.sleep(60)

    # Иначе, выходит сообщение о том, что время еще не подошло
    else:
        print("It's not time yet - " + moscow_time)
        time.sleep(600)
