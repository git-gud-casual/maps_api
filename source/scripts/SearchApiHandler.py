import requests
from source.scripts.ApiHandler import ApiHandler


class SearchApiHandler(ApiHandler):
    def __init__(self, url, params):
        super().__init__(url, params)

    # Новое подключение
    def new_response(self):
        self.response = requests.get(self.url, self.params)
        self.answer = self.response.json()['features'][0]

    # Возвращает координаты объекта
    def get_point(self):
        if self.get_status() == 200:
            return ','.join(map(str, self.answer['geometry']["coordinates"]))
        return False

    # Возвращает адрес объекта
    def get_address(self):
        if self.get_status() == 200:
            try:
                return self.answer['properties']['GeocoderMetaData']['text']
            except KeyError:
                try:
                    return self.answer['properties']["CompanyMetaData"]['address']
                except KeyError:
                    return 'отсутствует адрес организации'
        return False
