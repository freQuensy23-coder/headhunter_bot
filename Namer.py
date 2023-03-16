class Namer:
    @staticmethod
    def generate_name_skills(call_id):
        return f"{call_id}_skills.png"

    @staticmethod
    def generate_name_salary(call_id):
        return f"{call_id}_salary.png"

    @staticmethod
    def generate_name_vacancies_xlsx(call_id):
        return f"{call_id}_excel.xlsx"
