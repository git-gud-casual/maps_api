import requests
from source.scripts.ApiHandler import ApiHandler


class SearchApiHandler(ApiHandler):
    object_found = False

    def __init__(self, url, params, geocoder_handler):
        super().__init__(url, params)
        # Геокодер Api для адреса и индекс
        self.geocoder_handler = geocoder_handler

    # Новое подключение
    def new_response(self):
        super().new_response()
        self.answer = self.response.json()['features']
        if len(self.answer) > 0:
            self.object_found = True
            self.answer = self.response.json()['features'][0]
            # Устанавливаем новые координаты в параметре геокодера и подключаемся
            self.geocoder_handler.set_params(key=('geocode', self.get_point()))
            self.geocoder_handler.new_response()
        else:
            self.object_found = False

    # Возвращает координаты объекта
    def get_point(self):
        if self.get_status() == 200 and self.object_found:
            return ','.join(map(str, self.answer['geometry']["coordinates"]))
        return False

    # Возвращает адрес объекта
    def get_address(self):
        if self.object_found:
            return self.geocoder_handler.get_address()
        return 'Объект не найден'

    # Возвращает индекс объекта
    def get_index(self):
        if self.object_found:
            return self.geocoder_handler.get_index()
        return 'У ненайденного объекта не может быть индекса'
