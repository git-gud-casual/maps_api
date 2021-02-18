import requests
from source.scripts.ApiHandler import ApiHandler


# Класс для обработки запросов к Static Api
class StaticApiHandler(ApiHandler):
    # В конструктор класса передадим url, параметры и CacheHandler
    def __init__(self, url, params, cache_handler):
        super().__init__(url, params)
        self.url = url
        self.set_params(params)
        self.cache_handler = cache_handler

    # Метод получния карты
    def get_map(self):
        img_name = ';'.join(f'{key}-{self.params[key]}' for key in self.params.keys() if self.params[key]) + '.jpg'
        img = self.cache_handler.get_image(img_name)
        if img:
            return img
        # Устанавливаем соединение, т.к картинки нет в кеше
        self.response = requests.get(self.url, self.params)
        # Если подключения успешно, то загружаем карту
        if self.get_status() == 200:
            self.cache_handler.save_image(img_name, self.response.content)
            return self.cache_handler.get_image(img_name)
