# -*- coding: utf-8 -*-

from telebot import *
import telebot
import sqlite3
from sqlite3 import Error
from datetime import datetime
from telebot import types
import time


# Данные для входа
token = 'TOKEN'
bot = telebot.TeleBot(token)

# Создание ключевых кнопок меню
callback_button_today = types.KeyboardButton('Сегодня')
callback_button_tomorrow = types.KeyboardButton('Завтра')

# Добавление этих кнопок
date = telebot.types.ReplyKeyboardMarkup(True, True).row(callback_button_today, callback_button_tomorrow)

# Список для подсчета количества вызовов бота
# Используется в качестве добавления новых элементов, при нажатии кнопок "Сегодня"/"Завтра" и выводом ее длинны
entry = []

# Функция устанавливает контакт с базой данных SQLite3
# В случае ошибки происходит исключение и сообщение об этом
def create_connection(path):
	connect = None
	try:
		connect = sqlite3.connect(path)
		print("Connection to SQLite DB successful")
	except Error as e:
		print(f"The error '{e}' occurred")
	return connect


# Функция чтения данных в базе данных
# В случае ошибки происходит исключение и сообщение об этом
def execute_read_query(connect, query):
	cursor = connect.cursor()
	try:
		cursor.execute(query)
		result = cursor.fetchall()
		return result
	except Error as e:
		print(f"The error '{e}' occurred")


# Сама функция с запросом данных.
def look_for_hor():
	select_users = "SELECT * from users"
	horus = execute_read_query(connection, select_users)
	return horus


# Ловит все сообщения, адресованные боту
# Отвечает на них в случае совпадений написаного ниже
@bot.message_handler(content_types=["text"])
def Getting_up_to_speed(message):  # 15
	time_is = str(datetime.now())[:16]
	entry.append(1)
	print(time_is + ' - ' + str(len(entry)))
	if message.text:
		if message.text.lower() == 'сегодня':
			horoscope_td(message)
		elif message.text.lower() == 'завтра':
			horoscope_tm(message)
		else:
			bot.send_message(
				message.chat.id,
				('Привет ' + message.chat.first_name +
				 ', я рассказываю о твоем гороскопе - сегодняшнем и завтрашнем.\n'
				 'Если ты хочешь узнать подробнее, нажми на интересующий тебя \n'
				 'знак зодиака.\n'
				 'Но прежде, тебе надо выбрать день, который ты хочешь увидеть.'
				 )
			)
			time.sleep(8)
			bot.send_message(
				message.chat.id,
				'Если хочешь увидеть сегодняшний прогноз то нажми на кнопку (или напиши) сегодня/завтра.',
				reply_markup=date,
			)

# Если выбрана кнопка завтра, скрипт автоматически переводит 
# его в функцую ниже, и выводит кнопки знаков
@bot.callback_query_handler(func=lambda call: call.data == 'завтра')
def horoscope_tm(message):
	keys = types.InlineKeyboardMarkup()
	# И добавляем кнопку на экран
	key_o = types.InlineKeyboardButton(text='Овен', callback_data='Овен_завтра')
	# Готовим кнопки
	# По очереди готовим текст и обработчик для каждого знака зодиака.
	keys.add(key_o)
	key_t = types.InlineKeyboardButton(text='Телец', callback_data='Телец_завтра')
	keys.add(key_t)
	key_g = types.InlineKeyboardButton(text='Близнецы', callback_data='Близнец_завтра')
	keys.add(key_g)
	key_rk = types.InlineKeyboardButton(text='Рак', callback_data='Рак_завтра')
	keys.add(key_rk)
	key_lv = types.InlineKeyboardButton(text='Лев', callback_data='Лев_завтра')
	keys.add(key_lv)
	key_dev = types.InlineKeyboardButton(text='Дева', callback_data='Дева_завтра')
	keys.add(key_dev)
	key_li = types.InlineKeyboardButton(text='Весы', callback_data='Весы_завтра')
	keys.add(key_li)
	key_scorp = types.InlineKeyboardButton(text='Скорпион', callback_data='Скорпион_завтра')
	keys.add(key_scorp)
	key_sagit = types.InlineKeyboardButton(text='Стрелец', callback_data='Стрелец_завтра')
	keys.add(key_sagit)
	key_capr = types.InlineKeyboardButton(text='Козерог', callback_data='Казерог_завтра')
	keys.add(key_capr)
	key_vol = types.InlineKeyboardButton(text='Водолей', callback_data='Водолей_завтра')
	keys.add(key_vol)
	key_f = types.InlineKeyboardButton(text='Рыбы', callback_data='Рыба_завтра')
	keys.add(key_f)

	# Показываем все кнопки сразу и пишем сообщение о выборе
	bot.send_message(message.from_user.id, text='Выбери свой знак зодиака:', reply_markup=keys)

# Если выбрана кнопка сегодня, скрипт автоматически переводит 
# его в функцую ниже, и выводит кнопки знаков
@bot.callback_query_handler(func=lambda call: call.data == 'сегодня')
def horoscope_td(message):
	keyboard = types.InlineKeyboardMarkup()
	# Готовим кнопки
	# По очереди готовим текст и обработчик для каждого знака зодиака
	key_oven = types.InlineKeyboardButton(text='Овен', callback_data='Овен')
	# И добавляем кнопку на экран
	keyboard.add(key_oven)
	key_taurus = types.InlineKeyboardButton(text='Телец', callback_data='Телец')
	keyboard.add(key_taurus)
	key_gemini = types.InlineKeyboardButton(text='Близнецы', callback_data='Близнец')
	keyboard.add(key_gemini)
	key_rak = types.InlineKeyboardButton(text='Рак', callback_data='Рак')
	keyboard.add(key_rak)
	key_lev = types.InlineKeyboardButton(text='Лев', callback_data='Лев')
	keyboard.add(key_lev)
	key_deva = types.InlineKeyboardButton(text='Дева', callback_data='Дева')
	keyboard.add(key_deva)
	key_libra = types.InlineKeyboardButton(text='Весы', callback_data='Весы')
	keyboard.add(key_libra)
	key_scorpion = types.InlineKeyboardButton(text='Скорпион', callback_data='Скорпион')
	keyboard.add(key_scorpion)
	key_sagittarius = types.InlineKeyboardButton(text='Стрелец', callback_data='Стрелец')
	keyboard.add(key_sagittarius)
	key_capricorn = types.InlineKeyboardButton(text='Козерог', callback_data='Казерог')
	keyboard.add(key_capricorn)
	key_volley = types.InlineKeyboardButton(text='Водолей', callback_data='Водолей')
	keyboard.add(key_volley)
	key_fish = types.InlineKeyboardButton(text='Рыбы', callback_data='Рыба')
	keyboard.add(key_fish)

	# Показываем все кнопки сразу и пишем сообщение о выборе
	bot.send_message(message.from_user.id, text='Выбери свой знак зодиака:', reply_markup=keyboard)

# Делим данные из базы на 2 части, одна часть отвечает за сегоднящний день, 
# другая часть отвечает за завтрашний день.
hor_of_data = []
connection = create_connection("base_of_horoscope.sqlite")
hor_of_data.append(look_for_hor())  # Вызываем данные для разделения поровну
today, tomorrow = hor_of_data[0][:12], hor_of_data[0][12:]  # Делим данные поровну

# Функция для вывода данных по запросу кнопки
# Если длинна запроса меньше 9, то выводится сегодняшний гороскоп. Иначе завтрашний.
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	# Сегодняшний.
	if len(call.data) < 9:
		for look_for in today:
			if look_for[0] == call.data:
				bot.send_message(call.from_user.id, f"{look_for[0]}  {look_for[2]}.\n{look_for[1]}")
	# Завтрашний.
	elif len(call.data) > 9:
		ace = call.data[:len(call.data) - 7]
		for look_for in tomorrow:
			if str(look_for[0]) == ace:
				bot.send_message(call.from_user.id, f"{look_for[0]}  {look_for[2]}.\n{look_for[1]}")

if __name__ == '__main__':
	bot.polling(none_stop=True, interval=0)
