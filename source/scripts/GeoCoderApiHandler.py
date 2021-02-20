import requests
from source.scripts.ApiHandler import ApiHandler


class GeoCoderApiHandler(ApiHandler):
    answer = None
    object_found = False

    def __init__(self, url, params):
        super().__init__(url, params)

    # Устанавливает подключение
    def new_response(self):
        super().new_response()
        try:
            self.answer = self.response.json()["response"]["GeoObjectCollection"]["featureMember"][0]
            self.answer = self.answer["GeoObject"]
            self.object_found = True
        except KeyError:
            self.object_found = False

    # Получить адрес
    def get_address(self):
        if self.get_status() == 200 and self.object_found:
            return self.answer["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]
        return False

    # Получить индекс
    def get_index(self):
        if self.get_status() == 200 and self.object_found:
            try:
                return self.answer["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
            except KeyError:
                return 'индекс отсутствует'
        return False

    # Получить координаты
    def get_point(self):
        if self.get_status() == 200 and self.object_found:
            try:
                return ','.join(self.answer['Point']['pos'].split())
            except KeyError:
                pass
        return False

