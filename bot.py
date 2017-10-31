#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Сам бот


import telebot
import config
import database_management
import time
from telebot import types

# Ассоциируем переменную bot с нашим токеном
bot = telebot.TeleBot(config.token)
HELLO = 'hello'
NEW_EXPENSE = 'new_expense'
SET_EXPENSE = 'set_expense'
CANCEL = 'cancel'
CURRENT = 'current'
HELP = 'help'
THIS_MOMENT = 999999999   # тестим время работы cloud9


# ---- ХЕЛП ----
# Список команд
command_list = [HELP, CURRENT, NEW_EXPENSE, SET_EXPENSE, CANCEL]
# Словарь команд для хелпа
description_of = {HELP:'Прислать эту справку.', CURRENT:'Прислать текущий расход.',
             NEW_EXPENSE:'Добавить новый расход.', SET_EXPENSE: 'Установить значение расхода вручную.',
             CANCEL: 'Отменить последний расход.'}

# Введем переменную, отвечающую за сумму расхода
last_amount = 0

# ---- ПОДТЯГИВАЕМ БАЗУ ДАННЫХ ----

# db = database_management.db             # Храним словарь БД в database_management.py
db = database_management.file_in()      # Храним словарь БД локально. Если так, то в database_management.py надо убрать db


# ---- ФУНКЦИИ ----

def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    btn1 = types.KeyboardButton('Текущий расход 💵')
    btn2 = types.KeyboardButton('Добавить расход 💸')
    btn3 = types.KeyboardButton('Справка 📚')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Главное меню:', reply_markup=markup)

def change_db(id, value):
    global db, database_management
    db[id] = value
    database_management.file_out(db)


# Проверка существования профиля в базе данных. Если нету, создаем нулевой
def in_db(id):
    global db
    try:
        db[id] += 0
    except:
        db[id] = 0

# 3/3р/3 р./3₽/3 ₽/ 3 руб/... -> 3
def good_answer_to_number(string):
    try:
        num = int(string)
    except:
        i=0
        while string[i].isdigit() or string[i] == ' ':
            i += 1
        try :
            num = int(string[0:i])
        except:
            num = -1
    return(num)


# Отправить сообщение с текущим расходом
def show_current(message, db):
    in_db(message.chat.id)
    bot.send_message(message.chat.id, 'Ваш текущий расход - ' + str(db[message.chat.id]) + '₽.')


# ---- ОБРАБОТЧИКИ КОМАНД ----

@bot.message_handler(commands = ['start'])
def send_welcome(message):
    in_db(message.chat.id)
    bot.send_message(message.chat.id, 'Привет! Меня зовут Рэй, я помогу тебе контролировать твои расходы по кредитке!\n'
                                            'Твой текущий расход - '+str(db[message.chat.id])+'₽\n'
                                            'Чтобы получить справку нажми /' + HELP + '\n'
                                            'Если ты что-то растранжирил до нашего знакомства нажми на команду /'+SET_EXPENSE)
    main_menu(message)


@bot.message_handler(commands = [CURRENT])
def show_current_handler(message):
    show_current(message, db)
@bot.message_handler(regexp = 'Текущий расход 💵')
def show_current_text_handler(message):
    show_current(message, db)

@bot.message_handler(commands = [HELP])
def show_help(message):
    description = ''
    for i in command_list:
        description += '/' + i + ' - ' + description_of[i] + '\n'
    bot.send_message(message.chat.id, 'Я - бот-помощник для учета расхода по кредитке.\n'
                                      'Вот список моих вохможностей:\n' + description)
@bot.message_handler(regexp = 'Справка 📚')
def show_help_text(message):
    show_help(message)


@bot.message_handler(commands = [SET_EXPENSE])
def set_expense(message):
    bot.send_message(message.chat.id, 'Сколько?')
    bot.register_next_step_handler(message, set_expense1)
def set_expense1(message):
    temp = good_answer_to_number(message.text)  # Просто переменная, чтобы не ходить в функцию по несоклько раз
    if temp >= 0:
        change_db(message.chat.id, temp)
        show_current(message, db)
    else:
        bot.send_message(message.chat.id, 'Что-то ты не то ввел, дружище. \n'
                                          'Попробуем еще раз? /' + SET_EXPENSE)


@bot.message_handler(commands = [HELLO])
def welcome_back(message):
    bot.send_message(message.chat.id, 'С возвращением, ' + str(message.chat.first_name) + '! Рад снова видеть тебя :)')
    

@bot.message_handler(commands = [NEW_EXPENSE])
def add_expense(message):
    sent = bot.send_message(message.chat.id, 'Сколько потратил?\n'
                                             'Вводи только одно число, чтобы я не запутался')
    bot.register_next_step_handler(sent, add_expense1)
def add_expense1(message):
    global last_amount
    in_db(message.chat.id)
    temp = good_answer_to_number(message.text)  # Просто переменная, чтобы не ходить в функцию по несоклько раз
    if temp >= 0:
        last_amount = temp
        change_db(message.chat.id, db[message.chat.id] + last_amount)
        bot.send_message(message.chat.id, 'ОК, добавил твой новый расход.')
        show_current(message, db)
        bot.send_message(message.chat.id, 'Если мы с тобой что-то напутали, нажми /' + CANCEL)
    else:
        bot.send_message(message.chat.id, 'Что-то ты не то ввел, дружище. \n'
                                          'Попробуем еще раз? /'+NEW_EXPENSE)
@bot.message_handler(regexp = 'Добавить расход 💸')
def add_expense_text(message):
    add_expense(message)


@bot.message_handler(commands = [CANCEL])
def cancel(message):
    global last_amount
    try:
        change_db(message.chat.id, db[message.chat.id] - last_amount)
        bot.send_message(message.chat.id, 'Хорошо, отменяем последнюю сумму ('+str(last_amount)+'₽)')
        last_amount = 0
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так.')
    show_current(message, db)


# Время работы cloud9
@bot.message_handler(regexp = '[Зз]апомни этот момент')
def remember_this_moment(message):
    change_db(THIS_MOMENT, message.date)
    bot.send_message(message.chat.id, 'ОК, я запомнил время.')

@bot.message_handler(regexp = '[\s]*[Вв]ремя[\s]*работы[\s]*')
def work_time(message):
    bot.send_message(message.chat.id, 'Вот момент, который вы просили запомнить:\n'
                                      + time.ctime(db[THIS_MOMENT] + 10800) + ' (МСК)')


# ---- РЕЖИМ ОЖИДАНИЯ СООБЩЕНИЙ ----                  
if __name__ == '__main__':
     bot.polling(none_stop=True)




