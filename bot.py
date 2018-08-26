# -*- coding: utf-8 -*-

import calendar
import datetime
import locale

import telebot
import yaml

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

bot = telebot.TeleBot('TOKEN')

main_btns = ('📘 Cегодня', '📗 Завтра', '📅 Расписание на другие дни', '🔔 Расписание звонков')
week_btns = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Суббота', 'Воскресенье')

main_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.row(*main_btns[:2])
main_markup.row(main_btns[2])
main_markup.row(main_btns[3])

week_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
week_markup.row(*week_btns[:5])
week_markup.row(week_btns[5])
week_markup.row(week_btns[6])


@bot.message_handler(commands=['start'])
def welcome(message):
    text = 'Привет! Я помогу тебе узнать расписание, обращайся 😉'
    bot.send_message(message.chat.id, text, reply_markup=main_markup)


@bot.message_handler(func=lambda msg: msg.text in main_btns[:2])
def today_timetable(message):
    with open('timetable.yml', 'r') as f:
        timetable = yaml.load(f)
    tomorrow = message.text == main_btns[1]
    today = datetime.date.today() + datetime.timedelta(days=tomorrow)
    is_numerator = today.isocalendar()[1] % 2
    text = '*Расписание на {}:*\n'.format(message.text[2:].lower())
    try:
        text += '\n'.join(timetable[today.strftime("%a")][is_numerator])
    except KeyError:
        text += '\n'.join(timetable[today.strftime("%A")][is_numerator])
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: msg.text == main_btns[2])
def week_msg(message):
    bot.send_message(message.chat.id, 'Выберите день недели:', reply_markup=week_markup)


@bot.message_handler(func=lambda msg: msg.text in week_btns)
def week_timetable(message):
    with open('timetable.yml', 'r') as f:
        timetable = yaml.load(f)
    weekday = calendar.day_name[week_btns.index(message.text)].lower()
    text = '*Расписание на {}:*\n'.format(weekday if weekday[-1] != 'а' else weekday[:-1] + 'у')
    timetable = timetable[message.text]
    if timetable[0] == timetable[1]:
        text += '\n'.join(timetable[0])
    else:
        text += '*Числитель:*\n{}\n\n'.format('\n'.join(timetable[0]))
        text += '*Знаменатель*\n{}'.format('\n'.join(timetable[1]))
    bot.send_message(message.chat.id, text, reply_markup=main_markup, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: msg.text == main_btns[3])
def bells_msg(message):
    text = (
        '*Расписание звонков:*\n'
        '1. 8:00 - 9:35\n'
        '2. 9:45 - 11:20\n'
        '3. 11:30 - 13:05\n'
        '4. 13:25 - 15:00\n'
        '5. 15:10 - 16:45\n'
        '6. 16:55 - 18:30\n'
        '7. 18:40 - 20:00\n'
        '8. 20:10 - 21:30\n')
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: True)
def error_msg(message):
    bot.reply_to(message, 'К сожалению, я тебя не понимаю 😢', reply_markup=main_markup)


bot.polling()
