import json
import logging
import sys
from asyncio import sleep

from aiogram import Bot, Dispatcher, executor, types
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
    await message.reply(f"По вашему запросу найдено {loaded['found']} вакансий. Их обработка может занять некоторое (довольно большое) время. Результат будет отправлен по завершению работы")

    print("loaded ", loaded)
    # print("loaded items ", loaded.items())
    print("loaded items ", json.dumps(loaded['items'], indent=2))
    print("loaded pages ", json.dumps(loaded['pages'], indent=2))
    data = []
    for page in range(0, loaded['pages']):
        await sleep(1)
        params['page'] = page
        req = requests.get(HH_URL, params)
        loaded = json.loads(req.content.decode())
        data += loaded['items']

    ids = set() # Удаляет дубликаты по смежным тегам в запросах
    for vacancy in range(len(data) - 1, -1, -1):
        if data[vacancy]['id'] in ids:
            del data[vacancy]
        else:
            ids.add(data[vacancy]['id'])

    vacancies = [None for _ in range(len(data))]
    # pbar = tqdm(range(len(data)))
    num_vacancy = 0
    for index in tqdm(range(len(data))): # запросы к API hh.ru
        vacancy_url = f'https://api.hh.ru/vacancies/{data[index]["id"]}'
        print(data[index]["id"])
        req = requests.get(vacancy_url)
        vacancy_info = json.loads(req.content.decode())
        vacancies[index] = vacancy_info
        # num_vacancy += 1
        # pbar.set_postfix({'num_vacancy': num_vacancy})
        await sleep(1.2)

    print("vacancies ", vacancies)
    if not vacancies:
        await message.reply(f"По вашему запросу не найдено ни одной вакансии")
        sys.exit()
    namer = Namer()
    manager = ProcessHhData(namer)
    manager.get_necessery_skills(message, vacancies)
    manager.get_salary(message, vacancies)
    await message.reply(f"Обработка завершена")
    with open(namer.generate_name_skills(message), "rb") as photo:
        await message.reply_photo(photo)
    os.remove(namer.generate_name_skills(message))
    with open(namer.generate_name_salary(message), "rb") as photo:
        await message.reply_photo(photo)
    os.remove(namer.generate_name_salary(message))

    # with open(f"{message.from_id}_{message.message_id}.xlsx", 'rb') as exel:
    #     await bot.send_file()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
