from PyQt5.QtGui import QPixmap
import os


# Класс обработки кеша, чтобы не пришлось подключаться 100 раз за сеанс
class CacheHandler:
    def __init__(self, path):
        # Путь куда будут сохраняться картинки
        self.path = path

    # Получение карты
    def get_image(self, image_name):
        try:
            # Возвращаем картинку в случае ее присутствия в кеше
            open(self.path + image_name)
            return QPixmap(self.path + image_name)
        except FileNotFoundError:
            return False

    # Сохранение картинки
    def save_image(self, image_name, image):
        with open(self.path + image_name, 'wb') as img:
            img.write(image)
