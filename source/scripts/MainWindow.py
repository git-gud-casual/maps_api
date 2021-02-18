from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


# Класс главного окна
class MainWindow(QMainWindow):
    def __init__(self, static_handler, search_handler):
        super().__init__()
        # Загрузка интерфейс
        uic.loadUi('source/ui/MainWindow.ui', self)
        # Работать с ApiHandler удобнее в MainWindow
        self.static_api_handler = static_handler
        self.search_api_handler = search_handler

        self.set_map(self.static_api_handler.get_map())
        self.set_status(self.static_api_handler.get_status())
        self.ui_init()

    # Загрузка интерфейса
    def ui_init(self):
        # Группа RadioButton отвечающая за выбор типа карты (параметр l)
        self.l_param_but_group.buttonClicked.connect(self.type_map)
        # Поиск объекта
        self.find_object_but.clicked.connect(self.find_object)

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
        self.set_map(self.static_api_handler.get_map())
        self.set_status(self.static_api_handler.get_status())

    # Смена типы карты
    def type_map(self, button):
        if button.text() == 'Схема':
            key = ('l', 'map')
        elif button.text() == 'Спутник':
            key = ('l', 'sat')
        else:
            key = ('l', 'sat,skl')
        self.static_api_handler.set_params(key=key)
        self.new_img()

    # Найти объект
    def find_object(self):
        text = self.input_object.text()
        if text.replace(' ', '') != '':
            self.search_api_handler.set_params(key=('text', text))
            self.search_api_handler.new_response()
            if self.search_api_handler.get_status() == 200:
                point = self.search_api_handler.get_point()
                self.static_api_handler.set_params(key=('ll', point))
                self.static_api_handler.set_params(key=('pt', point + ',pm2wtm'))
                self.new_img()
                # Передаем ll в параметры для следуещего поиска
                self.search_api_handler.set_params(key=('ll', point))
                self.find_object_status.setText('Объект Найден')
            else:
                self.find_object_status.setText('Объект не найден')
        else:
            self.find_object_status.setText('Объект не введен')
