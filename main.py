
import telebot
import os
from flask import Flask, request
server = Flask(__name__)


bot = telebot.TeleBot("450973265:AAExas5j2FfvwU7BGjJ1NnE5uaARsoYpVT0")


def log(message,answer):
    print("/n ------")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \n Текст = {3}".format(message.from_user.first_name, message.from_user.last_name, str(message.from_user.id), message.text))


@bot.message_handler(commands=['help'])
def handle_text(message):
    answer = "Мои возможности ограничены,но так будет не долго!"
    log(message, answer)
    bot.send_message(message.chat.id, answer )

@bot.message_handler(commands=['start'])
def handle_text(message):
    answer = "Привет!"\
             "Рад приветствовать тебя в нашем прогресивном интернет-магазине ." \
             "Напиши мне 'хочу промокод' ,если горишь желанием его получить  "


    log(message, answer)
    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['settings'])
def handle_text(message):
    answer = "Тут пусто)"
    log(message, answer)
    bot.send_message(message.chat.id,answer )


@bot.message_handler(content_types=['text'])
def handle_text(message):

    if message.text == "хочу промокод" :
        answer = "Open20"
        log(message, answer)
        bot.send_message(message.chat.id, answer)


    elif message.text == "Хочу промокод":
        answer = "Open20"
        log(message, answer)
        bot.send_message(message.chat.id, answer)


    elif message.text == "Хочу промо код":
        answer = "Open20"
        log(message, answer)
        bot.send_message(message.chat.id, answer)
    elif message.text == "хочу промокод":
        answer = "Open20"
        log(message, answer)
        bot.send_message(message.chat.id, answer)

    elif message.text == " промо ":
        answer = "Open20"
        log(message, answer)
        bot.send_message(message.chat.id, answer)
    elif message.text == "Хочу промо-код ":
        answer = "Open20"
        log(message, answer)
        bot.send_message(message.chat.id, answer)
    elif message.text == "хочу промо код" :
        answer = "Open20"
        log(message, answer)
        bot.send_message(message.chat.id, answer)
    elif message.text == "хочу промо-код":
        answer = "Open20"
        log(message, answer)
        bot.send_message(message.chat.id, answer)
    else:

        bot.send_message(message.chat.id, "Не совем тебя понял")

@server.route("/450973265:AAExas5j2FfvwU7BGjJ1NnE5uaARsoYpVT0", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://robindickbot.herokuapp.com/450973265:AAExas5j2FfvwU7BGjJ1NnE5uaARsoYpVT0")
    return "!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
