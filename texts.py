import dataclasses

@dataclasses.dataclass
class Lang:
    @dataclasses.dataclass
    class EN:
        @dataclasses.dataclass
        class Messages:
            @dataclasses.dataclass
            class Registration:
                start_message = "Hello. I am bot. " \
                                "For get statistics from hh.ru by position just type his 'name'." \
                                "\nFor example type 'ruby' or 'Programmer' if you want to see what kind of skills employer search for these specialists." \
                                "Also type 'delivery' or 'engineer' if you are interested."

            class Company:
                telegram_link = "@JobHuntHelper"

    class RU:
        class Messages:
            @dataclasses.dataclass
            class Registration:
                start_message = "Hello. I am bot. " \
                                "For get statistics from hh.ru by position just type his 'name'." \
                                "\nFor example type 'ruby' or 'Programmer' if you want to see what kind of skills employer search for these specialists." \
                                "Also type 'delivery' or 'engineer' if you are interested."

            class Requests:
                not_correct_request = "К сожалению вакансий не найдено. Проверьте правильность запроса"
                start_grabbing_statistics = "Сейчас соберем статистику, ожидайте"
                decline_HH_query_send_another_request = "Запрос к серверу HeagHunter-а отменен, пожалуйста введите другой запрос"
            class Company:
                telegram_link = "@JobHuntHelper"