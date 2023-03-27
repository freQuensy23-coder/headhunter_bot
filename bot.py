import json
import logging
import sys
from asyncio import sleep
from typing import Text

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger# Add convinient library for logging
import requests
import pandas as pd
import seaborn as sns
from tqdm import tqdm

import texts
from config import *
from ProcessHhData import ProcessHhData
from Namer import Namer
# Configure logging
logging.basicConfig(level=logging.INFO)

sns.set(style='whitegrid', font_scale=1.3, palette='Set2')

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(texts.Messages.Registration.start_message)


# async def check
@dp.callback_query_handler(lambda callback_query: True)
async def callback_inline(call: types.CallbackQuery):
    if call.data == 'no':
        await call.message.answer("Хорошо")
    else:
        await call.message.answer("Сейчас соберем статичтику, ожидайте")
        name_plot_salary, name_plot_skills, name_excel = await process_hh_query(call.data, call.id)

        with open(name_plot_salary, "rb") as photo:
            await bot.send_photo(call.message.chat.id, photo)
        os.remove(name_plot_salary)
        with open(name_plot_skills, "rb") as photo:
            await bot.send_photo(call.message.chat.id, photo)
        os.remove(name_plot_skills)
        with open(name_excel, 'rb') as excel:
            await bot.send_document(call.message.chat.id, ('Вакансии.xlsx', excel))
        os.remove(name_excel)
    try:
        if call.message:
            pass

    except Exception as e:
        print(repr(e))

@dp.message_handler(content_types=["text"])
async def send_hh_search_query(message: types.Message):
    params = {
        'text': message.text,
        'area': 1,
        'page': 0,
        'per_page': 10
    }
    r = requests.get(HH_URL, params)
    loaded = json.loads(r.content.decode())

    if loaded["found"] == 0: # проерка если вакансий не найдено
        await message.reply(f"К сожалению вакансий не найдено. Проверьте правильность запроса")
        return


    btn = InlineKeyboardButton('Да', callback_data=message.text)
    btn2 = InlineKeyboardButton('Нет', callback_data='no')
    start_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    start_keyboard.add(btn, btn2)

    await message.reply(f"По вашему запросу найдено {loaded['found']}\
     вакансий. Их обработка может занять некоторое (довольно большое) время. Результат будет отправлен по завершению работы", reply_markup= start_keyboard)





async def process_hh_query(user_query, call_id):
    params = {
        'text': user_query,
        'area': 1,
        'page': 0,
        'per_page': 10
    }
    r = requests.get(HH_URL, params)
    loaded = json.loads(r.content.decode())
    data = []
    for page in range(0, loaded['pages']):
        await sleep(1)
        params['page'] = page
        req = requests.get(HH_URL, params)
        loaded = json.loads(req.content.decode())
        data += loaded['items']

    ids = set()  # Удаляет дубликаты по смежным тегам в запросах
    for vacancy in range(len(data) - 1, -1, -1):
        if data[vacancy]['id'] in ids:
            del data[vacancy]
        else:
            ids.add(data[vacancy]['id'])

    vacancies = [None for _ in range(len(data))]

    for index in tqdm(range(len(data))):  # запросы к API hh.ru
        vacancy_url = f'https://api.hh.ru/vacancies/{data[index]["id"]}'
        req = requests.get(vacancy_url)
        vacancy_info = json.loads(req.content.decode())
        vacancies[index] = vacancy_info
        await sleep(1.2)


    namer = Namer()
    process_data = ProcessHhData(namer)
    plot_skills = namer.generate_name_skills(call_id)
    process_data.get_necessery_skills(user_query, namer.generate_name_skills(call_id), vacancies)
    name_plot_salary = namer.generate_name_salary(call_id)
    process_data.get_salary(user_query, namer.generate_name_salary(call_id), vacancies)

    name_excel = namer.generate_name_vacancies_xlsx(call_id)
    process_data.genrate_excel(name_excel, vacancies)

    return plot_skills, name_plot_salary, name_excel

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
