import pandas as pd
import seaborn as sns


class ProcessHhData:
    @classmethod
    def get_necessery_skills(cls, message, vacancies):
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
        fig.savefig(f"{message.from_id}_{message.message_id}.png", bbox_inches="tight")