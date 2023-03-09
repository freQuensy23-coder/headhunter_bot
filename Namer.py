class Namer:
    @staticmethod
    def generate_name_skills(message):
        return f"{message.from_id}_{message.message_id}_skills.png"

    @staticmethod
    def generate_name_salary(message):
        return f"{message.from_id}_{message.message_id}_salary.png"
