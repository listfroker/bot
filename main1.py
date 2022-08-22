import telebot
from telebot import types
import pandas as pd
import time
import datetime

bot = telebot.TeleBot("5308655718:AAGUt0xaSAZTiMFEPHUFHxUkbqYcluKoDKg", parse_mode=None)

name = ""
childName = ""
complaint = ""

user_mailing = None



@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Здравствуйте, я бот помощник!\n", parse_mode='html')
    time.sleep(1)
    bot.send_message(message.from_user.id, 'Как я могу к вам обращаться?')
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, "Как зовут вашего ребенка?")
    bot.register_next_step_handler(message, get_childName)


def get_childName(message):
    global childName;
    global name;
    global user_mailing
    user_mailing = True
    childName = message.text;
    inMarkup = types.InlineKeyboardMarkup()
    inMarkup.add(types.InlineKeyboardButton('Перейти в главное меню', callback_data='choice1'))
    bot.send_message(message.from_user.id,f'{name}, спасибо, раз в месяц я буду связываться с вами в узнавать как прошел предыдущий месяц занятий. Вам удачи и желаю чтобы {childName} ждал(-a) с нетерпением наших следующих занятий!',reply_markup=inMarkup)


@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    try:
        if callback.message:
            if callback.data == "choice1":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                but1 = types.KeyboardButton("Завершить рассылку⛔")
                but2 = types.KeyboardButton("Жалобы/Предложения👂")
                markup.add(but1, but2)
                bot.send_message(callback.from_user.id, 'Вы в главном меню', reply_markup=markup)
    except Exception as e:
        print(repr(e))


@bot.message_handler(content_types=['text'])
def menu(message):
    if (message.text == "Завершить рассылку⛔"):
        bot.send_message(message.from_user.id, "Окей👌 Я больше не буду Вам писать.")
        global user_mailing
        user_mailing = False
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Возобновить рассылку")
        but2 = types.KeyboardButton("Жалобы/Предложения👂")
        markup.add(but1, but2)
        # bot.send_message(message.from_user.id, 'Вы в главном меню', reply_markup=markup)
    elif (message.text == "Жалобы/Предложения👂"):
        bot.send_message(message.from_user.id, "Подробно опишите ваше предложение/жалобу")


    elif (message.text == "Возобновить рассылку"):
        bot.send_message(message.from_user.id, "Вы возобновили рассылку")
        global user_mailing
        user_mailing = True
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Завершить рассылку⛔")
        but2 = types.KeyboardButton("Жалобы/Предложения👂")
        markup.add(but1, but2)
        # bot.send_message(message.from_user.id, 'Вы в главном меню', reply_markup=markup)







bot.infinity_polling()
