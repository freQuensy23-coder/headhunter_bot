import json
import logging
from asyncio import sleep

from aiogram import Bot, Dispatcher, executor, types
import requests
import pandas as pd
import seaborn as sns
from tqdm import tqdm

import texts
from config import *

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

    if loaded["found"] == 0:
        await message.reply(f"К сожалению вакансий не найдено. Проверьте правильность запроса")
        return
    await message.reply(f"По вашему запросу найдено {loaded['found']} вакансий. Их обработка может занять некоторое (довольно большое) время. Результат будет отправлен по завершению работы")

    data = []
    for page in range(1, loaded['pages']):
        await sleep(1)
        params['page'] = page
        req = requests.get(HH_URL, params)
        loaded = json.loads(req.content.decode())
        data += loaded['items']

    ids = set()
    for vacancy in range(len(data) - 1, -1, -1):
        if data[vacancy]['id'] in ids:
            del data[vacancy]
        else:
            ids.add(data[vacancy]['id'])

    vacancies = [None for _ in range(len(data))]
    for index in tqdm(range(len(data))):
        vacancy_url = f'https://api.hh.ru/vacancies/{data[index]["id"]}'

        req = requests.get(vacancy_url)
        vacancy_info = json.loads(req.content.decode())
        vacancies[index] = vacancy_info
        await sleep(0.9)

    vacancies_df = pd.json_normalize(vacancies) # ????
    data = pd.DataFrame(vacancies_df, columns=['id', 'name', 'description', 'key_skills', 'salary.from', 'salary.to',
                                               'salary.currency', 'salary.gross', 'address.lat', 'address.lng',
                                               'experience.id', 'employer.name',
                                               ])

    # data.to_excel(f"{message.from_id}_{message.message_id}.xlsx")

    skills = {}
    for i in range(len(data)):
        for skill in data.iloc[i]['key_skills']:
            if skill['name'] not in skills.keys():
                skills[skill['name']] = 0
            skills[skill['name']] += 1

    skills = pd.Series(skills).sort_values(ascending=False).head(15)
    top_skills = pd.DataFrame(skills).T
    plot = sns.barplot(top_skills, orient='h')
    plot.set(title=f'Top 15 skills"{message.text}"')
    fig = plot.get_figure()
    fig.savefig(f"{message.from_id}_{message.message_id}.png", bbox_inches="tight")

    await message.reply(f"Обработка завершена")
    with open(f"{message.from_id}_{message.message_id}.png", "rb") as photo:
        await message.reply_photo(photo)

    # with open(f"{message.from_id}_{message.message_id}.xlsx", 'rb') as exel:
    #     await bot.send_file()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
