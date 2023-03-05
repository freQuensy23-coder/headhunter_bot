import dataclasses


@dataclasses.dataclass
class Messages:
    @dataclasses.dataclass
    class Registration:
        start_message = "Hello. I am bot"