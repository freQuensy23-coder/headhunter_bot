import pandas as pd
import seaborn as sns
import warnings
from Namer import *


class ProcessHhData:
    # Namer namer
    def __init__(self, namer):
        self.namer = namer

    def get_necessery_skills(self, message, vacancies):
        vacancies_df = pd.json_normalize(vacancies)  # ????
        data = pd.DataFrame(vacancies_df,
                            columns=['id', 'name', 'description', 'key_skills', 'salary.from', 'salary.to',
                                     'salary.currency', 'salary.gross', 'address.lat', 'address.lng',
                                     'experience.id', 'employer.name',
                                     ])

        # data.to_excel(f"{message.from_id}_{message.message_id}.xlsx")

        skills = {}  #
        for i in range(len(data)):  # Подсчет скилов
            for skill in data.iloc[i]['key_skills']:
                if skill['name'] not in skills.keys():
                    skills[skill['name']] = 0
                skills[skill['name']] += 1

        skills = pd.Series(skills).sort_values(ascending=False).head(15)
        top_skills = pd.DataFrame(skills).T
        plot = sns.barplot(top_skills, orient='h')
        plot.set(title=f'Top 15 skills"{message.text}"')
        fig = plot.get_figure()  # рисуем график со скиллами

        fig.savefig(self.namer.generate_name_skills(message), bbox_inches="tight")

    # @classmethod

    def get_salary(self, message, vacancies):
        vacancies_df = pd.json_normalize(vacancies)

        data = pd.DataFrame(vacancies_df,
                            columns=['id', 'name', 'description', 'key_skills', 'salary.from', 'salary.to',
                                     'salary.currency', 'salary.gross', 'address.lat', 'address.lng',
                                     'experience.id', 'employer.name']) # оставляем нужные столбцы
        warnings.filterwarnings('ignore')

        salary_data = data.dropna(subset=['salary.from', 'salary.to'])  # отбрасываем строки с неуказанной зарплатой

        salary_data['salary'] = 0.5 * (salary_data['salary.from'] + salary_data[
            'salary.to'])  # оценим зарплату по вакансии как среднее между верхней и нижней

        usd_to_rub = 75.25 # зафиксируем курсы валют
        eur_to_rub = 80.1

        salary_data['salary'][salary_data['salary.currency'] == 'USD'] *= usd_to_rub  # переведем в рубли
        salary_data['salary'][salary_data['salary.currency'] == 'EUR'] *= eur_to_rub

        salary_data['salary'][salary_data['salary.gross']] *= 0.87 # вычтем ндфл

        # plot = sns.histplot(data=salary_data, x='salary').set(title='Распределение средней зп')
        plot = sns.histplot(data=salary_data, x='salary')
        plot.set(title="df")
        # plot.set(title=f'Distribution of salary"{message.text}"')
        fig = plot.figure  # рисуем график с заработной платой
        fig.savefig(self.namer.generate_name_salary(message), bbox_inches="tight")

