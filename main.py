import telebot



bot = telebot.TeleBot("450973265:AAExas5j2FfvwU7BGjJ1NnE5uaARsoYpVT0")

upd = bot.get_updates()
print (upd)
last_upd = upd[-1]
message_from_user = last_upd.message
print(message_from_user)

print(bot.get_me())

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



try:
    bot.polling(none_stop=True, interval=1)
except Exception:
    raise
