import threading
import time

from telebot import types, TeleBot
from telebot.types import *
from sqlite3 import connect

bot = TeleBot(token='secret')

keyb1 = types.ReplyKeyboardMarkup()
keyb1.add(KeyboardButton('Панель админа 😎'))

keyb2 = types.ReplyKeyboardMarkup(row_width=5)
keyb2.add(KeyboardButton('Артикул'), KeyboardButton('Название'),KeyboardButton('Количество'))
keyb2.add(KeyboardButton('Назад'))

keyb3 = ReplyKeyboardMarkup(row_width=5)
keyb3.add(KeyboardButton('Назад'))

@bot.message_handler(commands=['start'])
def start(message):

    """
    conn = connect("data.db")
    id = message.from_user.id
    cursor = conn.execute("SELECT * FROM users WHERE Id = ?", [id])
    if not cursor.fetchall():
        conn.execute("INSERT INTO users VALUES (?)", [id])
        conn.commit()
    """

    bot.send_message(message.from_user.id, f"Здравствуйте, {message.from_user.first_name} рады Вас видеть", reply_markup=keyb1)
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Деталь 1', callback_data='1')
    button2 = types.InlineKeyboardButton('Деталь 2', callback_data='2')
    button3 = types.InlineKeyboardButton('Деталь 3', callback_data='3')
    button4 = types.InlineKeyboardButton('Деталь 4', callback_data='4')
    button5 = types.InlineKeyboardButton('Деталь 5', callback_data='5')
    button6 = types.InlineKeyboardButton('Деталь 6', callback_data='6')
    button7 = types.InlineKeyboardButton('Деталь 7', callback_data='7')
    markup.row(button1, button2, button3)
    markup.row(button4, button5, button6, button7)
    photo = open('photo.jpg', 'rb')
    bot.send_photo(message.chat.id, photo, reply_markup=markup)

@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.from_user.id, "Фото:", reply_markup=keyb1)
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Деталь 1', callback_data='1')
    button2 = types.InlineKeyboardButton('Деталь 2', callback_data='2')
    button3 = types.InlineKeyboardButton('Деталь 3', callback_data='3')
    button4 = types.InlineKeyboardButton('Деталь 4', callback_data='4')
    button5 = types.InlineKeyboardButton('Деталь 5', callback_data='5')
    button6 = types.InlineKeyboardButton('Деталь 6', callback_data='6')
    button7 = types.InlineKeyboardButton('Деталь 7', callback_data='7')
    markup.row(button1, button2, button3)
    markup.row(button4, button5, button6, button7)
    photo = open('photo.jpg', 'rb')
    bot.send_photo(message.chat.id, photo, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    conn = connect("data.db")
    bot.answer_callback_query(callback_query_id=call.id)
    cursor = conn.execute("SELECT * FROM details WHERE Ide = ?", [call.data])
    answer = cursor.fetchall()
    print(answer)
    bot.send_message(call.message.chat.id, f"✅{str(answer[0][0])}. " + 'Артикул: ' + str(answer[0][1]) + '; Название: ' + str(answer[0][2]) + '; Количество: ' + str(answer[0][3]) + '; Прочность: ' + str(answer[0][4]))

@bot.message_handler(content_types=['text'])
def process_message(message):
    if message.text == 'Панель админа 😎':
        bot.send_message(message.chat.id, 'Введите пароль')
        bot.register_next_step_handler(message, prov)
    else:
        bot.send_message(message.chat.id, "Введённое сообщение неизвестно, попробуйте еще раз", reply_markup=keyb1)

def save_art(message, mess):  # message.text
    if str(message.text) == 'Назад':
        bot.send_message(message.chat.id, 'Вы перенесены', reply_markup=keyb1)
    else:
        conn = connect("data.db")
        cursor = conn.execute("UPDATE details SET Art = ? WHERE Ide = ? ", [message.text, mess])
        bot.send_message(message.chat.id, 'Артикул обновлен ', reply_markup=keyb1)
        conn.commit()

def save_name(message, mess):  # message.text
    if str(message.text) == 'Назад':
        bot.send_message(message.chat.id, 'Вы перенесены', reply_markup=keyb1)
    else:
        conn = connect("data.db")
        cursor = conn.execute("UPDATE details SET Name = ? WHERE Ide = ? ", [message.text, mess])
        bot.send_message(message.chat.id, 'Имя обновлено ', reply_markup=keyb1)
        conn.commit()  # desired

def save_col(message, mess):  # message.text
    if str(message.text) == 'Назад':
        bot.send_message(message.chat.id, 'Вы перенесены', reply_markup=keyb1)
    else:
        conn = connect("data.db")
        cursor = conn.execute("UPDATE details SET Col = ? WHERE Ide = ? ", [message.text, mess])
        bot.send_message(message.chat.id, 'Количество обновлено ', reply_markup=keyb1)
        conn.commit()  # desired

def save_numb(message):  # message.text
    string = message.text
    if str(message.text) == 'Назад':
        bot.send_message(message.chat.id, 'Вы перенесены', reply_markup=keyb1)
    elif string.isdigit() == True and int(message.text) < 8:
        bot.send_message(message.chat.id, f'Выберете что изменить детали №{message.text}', reply_markup=keyb2)
        bot.register_next_step_handler(message, help, message.text)
    else:
        bot.send_message(message.chat.id,f'Неизвестный номер {message.text}')

def prov(message):
    if message.text == "reg12345":
        bot.send_message(message.chat.id, 'Введите номер детали для изменений', reply_markup=keyb3)
        bot.register_next_step_handler(message, save_numb)
    else:
        bot.send_message(message.chat.id, 'Неверный пароль')
def help(message, num):
    if str(message.text) == 'Назад':
        bot.send_message(message.chat.id, 'Вы перенесены', reply_markup=keyb1)
    elif message.text == 'Артикул':
        bot.send_message(message.chat.id, 'Введите номер новый артикул для этой детали')
        bot.register_next_step_handler(message, save_art, num)
    elif message.text == 'Название':
        bot.send_message(message.chat.id, 'Введите новое название для этой детали')
        bot.register_next_step_handler(message, save_name, num)
    elif message.text == 'Количество':
        bot.send_message(message.chat.id, 'Введите новое количество для этой детали')
        bot.register_next_step_handler(message, save_col, num)

"""
def updater():
    while True:
        try:
            conn = connect("data.db")  # поисковый запрос, args вместо form, тк тип запроса - GET
            art = conn.execute("SELECT Art FROM details")
            tab_art = art.fetchall()
            rep = conn.execute("SELECT Repair FROM details")
            tab_rep = rep.fetchall()
            col = conn.execute("SELECT Col FROM details")
            tab_col = col.fetchall()
            id = conn.execute("SELECT Id FROM users")
            tab_id = rep.fetchall()
            for i in range(len(tab_art)):
                conn = connect("data.db")
                conn.execute("UPDATE details SET Repair = ? WHERE Art = ? ", [int(tab_rep[i][0]) - 1, tab_art[i][0]])
                conn.commit()
                if int(tab_rep[i][0]) < 52:
                    for a in range(len(tab_id)):  # tab_id[i][0]
                        conn = connect("data.db")
                        bot.send_message(tab_id[i][0], f'Оборудование с артикулом {tab_art[i][0]} сломана')
                if int(tab_rep[i][0]) < 2:
                    for a in range(len(tab_id)):  # tab_id[i][0]
                        conn = connect("data.db")
                        bot.send_message(tab_id[a][0], f'Оборудование с артикулом {tab_art[i][0]} стало металлоломом')
                        conn.execute("UPDATE details SET Col = ? WHERE Art = ? ",
                                     [int(tab_col[i][0]) - 1, tab_art[i][0]])
                        conn.commit()

        except Exception as e:
            print("error", e)
        time.sleep(600)

t = threading.Thread(target=updater)
t.start()
"""

bot.infinity_polling()
