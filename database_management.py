# Читаем и пишем базу данных

import config
#import time


# ---- БАЗА ДАННЫХ ----
#  функции in и out считывают базу данных в словарь с ключами айдишниками
#  и значениями расходами за текущий месяц.


def file_in():
    fin = open(config.database,'r')
    db = [line.strip().split() for line in fin.readlines()]
    db = {int(profile[0]):int(profile[1]) for profile in db}
    fin.close()
    return db


def file_out(db):
    fout = open(config.database, 'w')
    for key in db.keys():
        print(str(key) + ' ' + str(db[key]), file=fout)
    fout.close()




# ----  ПЕРИОДИЧЕСКАЯ СИНХРОНИЗАЦИЯ С БД ----
#while True:
#    file_out(db)
#    time.sleep(60)