from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


# Класс главного окна
class MainWindow(QMainWindow):
    def __init__(self, map_, status_code):
        super().__init__()
        # Загрузка интерфейс
        uic.loadUi('source/ui/MainWindow.ui', self)
        if map_:
            self.set_map(map_)
        self.set_status(status_code)

    # Метод для отображения карты на QLabel
    def set_map(self, map_):
        # self.map_render - QLabel для отображения карты
        self.map_render.setPixmap(map_)

    # Оторбражение статус кода. Для отладки
    def set_status(self, msg):
        self.error_label.setText(f'Status-code:\n{msg}')
