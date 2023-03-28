import dataclasses


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
