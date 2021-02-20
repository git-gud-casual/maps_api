import requests
from source.scripts.ApiHandler import ApiHandler
from source.scripts.distance import lonlat_distance


class SearchApiHandler(ApiHandler):
    object_found = False

    def __init__(self, url, params, geocoder_handler):
        super().__init__(url, params)
        # Геокодер Api для адреса и индекс
        self.geocoder_handler = geocoder_handler

    # Новое подключение
    def new_response(self, pos=None):

        self.geocoder_handler.new_response()
        self.set_params(key=('text', self.geocoder_handler.get_address()))
        super().new_response()
        if self.get_status() == 200 and \
                self.response.json()['properties']['ResponseMetaData']['SearchResponse']['found'] > 0:
            self.answer = self.response.json()['features']
            # Просматриваем все организации в 50м
            for i in self.answer:

                print(lonlat_distance(i['geometry']["coordinates"],
                                   tuple(map(
                                       float, self.geocoder_handler.get_point().split(',')))))
                if lonlat_distance(i['geometry']["coordinates"],
                                   tuple(map(
                                       float, self.geocoder_handler.get_point().split(',')))) <= 50:
                    print(pos)
                    self.answer = i
                    # Устанавливаем новые координаты в параметре геокодера и подключаемся
                    # Это нужно для вывода индекса и адреса в дальнейшем
                    self.geocoder_handler.set_params(key=('geocode', self.get_point()))
                    self.geocoder_handler.new_response()
                    self.object_found = True
                    return
            self.object_found = False
        else:
            self.object_found = False

    # Возвращает координаты объекта
    def get_point(self):
        if self.get_status() == 200 and self.answer:
            return ','.join(map(str, self.answer['geometry']["coordinates"]))
        return False
