import requests
from source.scripts.ApiHandler import ApiHandler


class GeoCoderApiHandler(ApiHandler):
    answer = None

    def __init__(self, url, params):
        super().__init__(url, params)

    # Устанавливает подключение
    def new_response(self):
        super().new_response()
        self.answer = self.response.json()["response"]["GeoObjectCollection"]["featureMember"]
        self.answer = self.answer[0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]

    # Получить адрес
    def get_address(self):
        if self.get_status() == 200:
            return self.answer["Address"]["formatted"]
        return False

    # Получить индекс
    def get_index(self):
        if self.get_status() == 200:
            try:
                return self.answer["Address"]["postal_code"]
            except KeyError:
                return 'индекс отсутствует'
        return False
