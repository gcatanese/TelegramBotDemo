
class User:
    def __init__(self, id):
        self.id = id
        self.first_name = ""
        self.last_name = ""
        self.lang = ""

    def __init__(self):
        self.id = ""
        self.first_name = ""
        self.last_name = ""
        self.lang = ""

    def get_full_name_and_lang(self):
        return f'{self.first_name} {self.last_name} ({self.lang})'

    def __str__(self):
        return f"id:{self.id} first_name:{self.first_name} last_name:{self.last_name} lang:{self.lang}"


class TextMessage:
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"message:{self.message}"


class MultiItems:

    def __init__(self):
        self.message = ""
        self.items = []

    def __init__(self, message, items):
        self.message = message
        self.items = items

    def __str__(self):
        return f"message:{self.message} items:{self.items}"



