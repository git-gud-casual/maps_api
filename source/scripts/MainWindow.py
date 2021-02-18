from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


# Класс главного окна
class MainWindow(QMainWindow):
    def __init__(self, handler):
        super().__init__()
        # Загрузка интерфейс
        uic.loadUi('source/ui/MainWindow.ui', self)
        # Работать с ApiHandler удобнее в MainWindow
        self.handler = handler

        self.set_map(self.handler.get_map())
        self.set_status(self.handler.get_status())
        self.ui_init()

    # Загрузка интерфейса
    def ui_init(self):
        # Группа RadioButton отвечающая за выбор типа карты (параметр l)
        self.l_param_but_group.buttonClicked.connect(self.type_map)

    # Метод для отображения карты на QLabel
    def set_map(self, map_):
        # self.map_render - QLabel для отображения карты
        if map_:
            self.map_render.setPixmap(map_)

    # Оторбражение статус кода. Для отладки
    def set_status(self, msg):
        self.error_label.setText(f'Status-code:\n{msg}')

    # Отображение нового изображения
    def new_img(self):
        self.set_map(self.handler.get_map())
        self.set_status(self.handler.get_status())

    def type_map(self, button):
        if button.text() == 'Схема':
            key = ('l', 'map')
        elif button.text() == 'Спутник':
            key = ('l', 'sat')
        else:
            key = ('l', 'sat,skl')
        self.handler.set_params(key=key)
        self.new_img()
