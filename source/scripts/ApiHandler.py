import requests


# Класс родитель для других обработчиков API
class ApiHandler:
    def __init__(self, url, params):
        self.response = None
        self.url = url
        self.params = params

    # Метод для установки параметров
    def set_params(self, params=None, key=None):
        if params:
            self.params = params
        else:
            # Можно изменить лишь один параметр, просто передав аргумент key
            self.params[key[0]] = key[1]

    # Метод для получения статус-кода
    def get_status(self):
        if self.response:
            return self.response.status_code
        return 'not connected'

    def new_response(self):
        self.response = requests.get(self.url, self.params)
