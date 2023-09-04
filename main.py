from telebot import TeleBot
from telebot.types import *
from datetime import *
import pytz
import os
import pandas as pd

bot = TeleBot("5972048412:AAH8m9E6ZznzHxwjvrDA_ipAasiBfYsVdmE")

admin = "matveygal"

forbidden = list(map(lambda x: x.replace("\n", ""), open("Data/forbidden.txt", "r").readlines()))



class User:
    def __init__(self, msg):
        self.chat_id = msg.chat.id
        self.username = str(msg.chat.username)
        self.tg_first_name = msg.chat.first_name
        self.tg_last_name = msg.chat.last_name
        self.first_date = datetime.now(pytz.timezone('Europe/Moscow'))


@bot.message_handler(commands=["start"])
def start(msg):

    menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_kb.add(KeyboardButton("Все преподы📃"))

    bot.send_message(msg.chat.id,
                     "Привет! Это бот который позволяет искать досье на преподавателей от L2Hub быстро и удобно. Создал его @matveygal по своему желанию и от скуки. Еще этот @matveygal может написать вам бота но не бесплатно.\n\nТы можешь ввести имя, фамилию, кусок отчества и т.п. любого препода, досье на которого уже выпустил L2Hub, и бот его тебе выдаст.",
                     reply_markup=menu_kb)

    data = pd.read_excel("Data/info.xlsx")
    if msg.chat.id not in data["chat id"].tolist():
        new_row = {"Username": "@" + str(msg.chat.username),
                   "first name": str(msg.chat.first_name),
                   "last name": str(msg.chat.last_name),
                   "chat id": str(msg.chat.id),
                   "first_date": str(datetime.now(pytz.timezone('Europe/Moscow')))[0:19]}
        data = data.append(new_row, ignore_index=True)
        data.to_excel("Data/info.xlsx", index=False)





@bot.message_handler(commands=["info"])
def info(msg):
    if msg.chat.username == admin:
        bot.send_document(msg.chat.id, open("Data/Info.xlsx", "rb"),
                          caption="Вот табличка с данными пользователей, которая обновляется каждый раз когда в бота заходит новый пользователь.")

    else:
        bot.send_message(msg.chat.id, "Ахахаххаха нельзя! Можно только @matveygal!")



@bot.message_handler(content_types=["text"])
def inp(msg):

    if msg.text == "Все преподы📃":

        all_teachers_kb = InlineKeyboardMarkup()

        listochek = os.listdir("teachers")

        for i in listochek:
            all_teachers_kb.add(InlineKeyboardButton(text=i[:-4],
                                                     callback_data=str(listochek.index(i))))

        bot.send_message(msg.chat.id,
                         "Вот список всех преподов на которых L2Hub публиковал досье.\nВы можете тыкнуть на препода чтобы просмотреть досье на него:",
                         reply_markup=all_teachers_kb)

        back_to_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        back_to_menu_kb.add(KeyboardButton("Назад в меню🔙"))

        bot.send_message(msg.chat.id,
                         "Если надо - выйди в меню",
                         reply_markup=back_to_menu_kb)

    elif msg.text == "Назад в меню🔙":

        menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        menu_kb.add(KeyboardButton("Все преподы📃"))

        bot.send_message(msg.chat.id,
                         "Это меню бота. Тут ты можешь ввести имя, фамилию, кусок отчества и т.п. любого препода, досье на которого уже выпустил L2Hub, и бот его тебе выдаст",
                         reply_markup=menu_kb)

    else:

        if len(msg.text) >= 3:

            listochek = os.listdir("teachers")

            sent = False

            for i in listochek:

                if msg.text.lower() in i[:-4].lower():

                    bot.send_photo(msg.chat.id,
                                   open(rf"teachers/{i}", "rb"))

                    sent = True

            if not sent:

                bot.send_message(msg.chat.id,
                                 "По вашему запросу ничего не найдено.")

        else:

            bot.send_message(msg.chat.id, "Так нельзя. Запросы меньше трёх символов не имеют смысла и излишне нагружают систему, так что я их запретил аххахах.")



@bot.callback_query_handler(func=lambda call: True)
def answer(call):

    listochek = os.listdir("teachers")

    bot.send_photo(call.message.chat.id, open(rf"teachers/{listochek[int(call.data)]}", "rb"))


bot.infinity_polling()
