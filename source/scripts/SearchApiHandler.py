import requests
from source.scripts.ApiHandler import ApiHandler


class SearchApiHandler(ApiHandler):
    def __init__(self, url, params):
        super().__init__(url, params)

    # Новое подключение
    def new_response(self):
        self.response = requests.get(self.url, self.params)
        self.answer = self.response.json()

    # Возвращает координаты объекта
    def get_point(self):
        if self.get_status() == 200:
            return ','.join(map(str, self.answer['features'][0]['geometry']["coordinates"]))
        return False
