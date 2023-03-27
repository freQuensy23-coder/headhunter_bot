import numpy as np
import pandas as pd
import seaborn as sns
import warnings
from loguru import logger

from matplotlib import pyplot as plt
from matplotlib.ticker import AutoLocator

from Namer import Namer


class ProcessHhData:
    def __init__(self, namer):
        self.namer = namer

    def get_necessery_skills(self, user_query, name_saved_file, vacancies):
        vacancies_df = pd.json_normalize(vacancies)  # ????
        data = pd.DataFrame(vacancies_df,
                            columns=['id', 'name', 'description', 'key_skills', 'salary.from', 'salary.to',
                                     'salary.currency', 'salary.gross', 'address.lat', 'address.lng',
                                     'experience.id', 'employer.name',
                                     ])

        skills = {}  #
        for i in range(len(data)):  # Подсчет скилов
            for skill in data.iloc[i]['key_skills']:
                if skill['name'] not in skills.keys():
                    skills[skill['name']] = 0
                skills[skill['name']] += 1

        skills = pd.Series(skills).sort_values(ascending=False).head(15)

        top_skills = pd.DataFrame(skills).T
        plot = sns.barplot(top_skills, orient='h')
        plot.set(title=f'Top 15 skills"{user_query}"')
        fig = plot.get_figure()  # рисуем график со скиллами

        fig.savefig(name_saved_file, bbox_inches="tight")
        fig, ax1 = plt.subplots()
        ax1.yaxis.set_major_locator(AutoLocator())
        logger.info(f"Skills diagram has been drawn")
    # @classmethod

    def get_salary(self, user_query, name_saved_file, vacancies):
        vacancies_df = pd.json_normalize(vacancies)

        data = pd.DataFrame(vacancies_df,
                            columns=['id', 'name', 'description', 'key_skills', 'salary.from', 'salary.to',
                                     'salary.currency', 'salary.gross', 'address.lat', 'address.lng',
                                     'experience.id', 'employer.name'])  # оставляем нужные столбцы

        salary_data = data.dropna(subset=['salary.from', 'salary.to'])  # отбрасываем строки с неуказанной зарплатой

        salary_data['salary'] = 0.5 * (salary_data['salary.from'] + salary_data[
            'salary.to'])  # оценим зарплату по вакансии как среднее между верхней и нижней

        usd_to_rub = 75.25  # зафиксируем курсы валют
        eur_to_rub = 80.1

        salary_data['salary'][salary_data['salary.currency'] == 'USD'] *= usd_to_rub  # переведем в рубли
        salary_data['salary'][salary_data['salary.currency'] == 'EUR'] *= eur_to_rub

        salary_data['salary'][salary_data['salary.gross']] *= 0.87  # вычтем ндфл

        counts, bins = np.histogram(salary_data['salary'])
        p = plt.stairs(counts, bins)
        uc = np.unique(counts)

        fig, ax1 = plt.subplots()
        ax1.set(yticks=uc)
        fig = p.figure  # рисуем график с заработной платой

        fig.savefig(name_saved_file, bbox_inches="tight")
        logger.info(f"Salary diagram has been drawn")

    def genrate_excel(self, name_saved_file, vacancies):
        vacancies_df = pd.json_normalize(vacancies)

        data = pd.DataFrame(vacancies_df,
                            columns=['id', 'name', 'description', 'key_skills', 'salary.from', 'salary.to',
                                     'salary.currency', 'salary.gross', 'address.lat', 'address.lng',
                                     'experience.id', 'employer.name'])  # оставляем нужные столбцы
        data.to_excel(name_saved_file)
        logger.info(f"Excel file has been created")
