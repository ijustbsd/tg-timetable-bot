# -*- coding: utf-8 -*-

import datetime
import os

import yaml
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv('TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

main_btns = ('📘 Cегодня', '📗 Завтра', '📅 Расписание на другие дни', '🔔 Расписание звонков')
week_btns = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Суббота', 'Воскресенье')

main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.row(*(types.KeyboardButton(text) for text in main_btns[:2]))
main_markup.row(types.KeyboardButton(main_btns[2]))
main_markup.row(types.KeyboardButton(main_btns[3]))

week_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
week_markup.row(*(types.KeyboardButton(text) for text in week_btns[:5]))
week_markup.row(types.KeyboardButton(week_btns[5]))
week_markup.row(types.KeyboardButton(week_btns[6]))


def parser(src):
    return ['{}\n`({}, {})`'.format(*x) if isinstance(x, list) else x for x in src]


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    text = 'Привет! Я помогу тебе узнать расписание, обращайся 😉'
    await bot.send_message(message.chat.id, text, reply_markup=main_markup)


@dp.message_handler(text=main_btns[:2])
async def today_timetable(message: types.Message):
    with open('timetable.yml', 'r') as f:
        timetable = yaml.safe_load(f)
    tomorrow = message.text == main_btns[1]
    today = datetime.date.today() + datetime.timedelta(days=tomorrow)
    is_numerator = not today.isocalendar()[1] % 2
    text = '*Расписание на {}:*\n'.format(message.text[2:].lower())
    text += '\n'.join(parser(timetable[today.strftime("%A")][is_numerator]))
    await bot.send_message(message.chat.id, text, parse_mode='Markdown')


@dp.message_handler(text=[main_btns[2]])
async def week_msg(message: types.Message):
    await bot.send_message(message.chat.id, 'Выберите день недели:', reply_markup=week_markup)


@dp.message_handler(text=week_btns)
async def week_timetable(message: types.Message):
    with open('timetable.yml', 'r') as f:
        timetable = yaml.safe_load(f)
    index = week_btns.index(message.text)
    ru = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')
    text = '*{}:*\n'.format(ru[index])
    timetable = tuple(timetable.values())[index]
    if timetable[0] == timetable[1]:
        text += '\n'.join(parser(timetable[0]))
    else:
        text += '*Числитель:*\n{}\n\n'.format('\n'.join(parser(timetable[0])))
        text += '*Знаменатель*\n{}'.format('\n'.join(parser(timetable[1])))
    await bot.send_message(message.chat.id, text, reply_markup=main_markup, parse_mode='Markdown')


@dp.message_handler(text=[main_btns[3]])
async def bells_msg(message: types.Message):
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
    await bot.send_message(message.chat.id, text, parse_mode='Markdown')


@dp.message_handler()
async def error_msg(message: types.Message):
    await message.answer('К сожалению, я тебя не понимаю 😢', reply_markup=main_markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
