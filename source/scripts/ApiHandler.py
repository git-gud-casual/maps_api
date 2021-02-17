import requests


# Класс для обработки запросов
class ApiHandler:
    response = None

    # В конструктор класса передадим url, параметры и CacheHandler
    def __init__(self, url, params, cache_handler):
        self.url = url
        self.set_params(params)
        self.cache_handler = cache_handler

    # Метод для установки параметров
    def set_params(self, params):
        self.params = params

    # Метод для получения статус-кода
    def get_status(self):
        if self.response:
            return self.response.status_code
        return 'not connected'

    # Метод получния карты
    def get_map(self):
        img_name = ';'.join(f'{key}-{self.params[key]}' for key in self.params.keys()) + '.jpg'
        img = self.cache_handler.get_image(img_name)
        if img:
            return img
        # Устанавливаем соединение, т.к картинки нет в кеше
        self.response = requests.get(self.url, self.params)
        # Если подключения успешно, то загружаем карту
        if self.get_status() == 200:
            self.cache_handler.save_image(img_name, self.response.content)
            return self.cache_handler.get_image(img_name)
