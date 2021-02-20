from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt


# Класс главного окна
class MainWindow(QMainWindow):
    def __init__(self, static_handler, search_handler, geocoder_handler):
        super().__init__()
        # Загрузка интерфейс
        uic.loadUi('source/ui/MainWindow.ui', self)
        # Работать с ApiHandler удобнее в MainWindow
        self.static_api_handler = static_handler
        self.search_api_handler = search_handler
        self.geocoder_api_handler = geocoder_handler

        # Размеры QLabel для отображения карты. Понадобится для отслеживания кликов
        self.MAP_RENDER_SIZE = (self.map_render.width(), self.map_render.height())

        self.set_map(self.static_api_handler.get_map())
        self.set_status(self.static_api_handler.get_status())
        self.ui_init()

    # Загрузка интерфейса
    def ui_init(self):
        # Группа RadioButton отвечающая за выбор типа карты (параметр l)
        self.l_param_but_group.buttonClicked.connect(self.type_map)
        # Поиск объекта
        self.find_object_but.clicked.connect(self.find_object)
        # Сброс найденного объекта
        self.clear_object_but.clicked.connect(self.clear_object)
        # Добавить индекс к адресу
        self.add_index.stateChanged.connect(self.index)

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
    def find_object(self, point=False, responsed=False):
        if not point:
            text = self.input_object.text()
        else:
            text = point
        if text.replace(' ', '') != '' or responsed:
            # Устанавливаем соединение с GeocoderApi
            if not responsed:
                self.geocoder_api_handler.set_params(key=('geocode', text))
                self.geocoder_api_handler.new_response()
            point = self.geocoder_api_handler.get_point()
            if point:
                self.set_new_object(point)
                self.address_text.setPlainText('Адрес: \n' +
                                               "\n".join(self.geocoder_api_handler.get_address().split(", ")))
            else:
                self.address_text.setPlainText('Объект не найден')
        else:
            self.address_text.setPlainText('Объект не введен')

    # Установить новый объект на карте
    def set_new_object(self, point):
        self.static_api_handler.set_params(key=('ll', point))
        self.static_api_handler.set_params(key=('pt', point + ',pm2wtm'))
        self.new_img()

    # Сброс найденного объекта
    def clear_object(self):
        self.static_api_handler.set_params(key=('pt', None))
        self.new_img()
        self.input_object.setText('')
        self.address_text.setPlainText('')
        self.add_index.setCheckState(False)

    # Добавить индекс
    def index(self):
        if self.address_text.toPlainText() and self.geocoder_api_handler.get_index():
            if self.add_index.isChecked():
                self.address_text.appendPlainText(f'Индекс: {self.geocoder_api_handler.get_index()}')
            else:
                self.address_text.setPlainText('\n'.join(
                    self.address_text.toPlainText().split('\n')[:-1:]))
        else:
            # Если адреса нет, то переводим CheckBox в False
            self.add_index.setCheckState(False)

    # Событии мыши
    def mousePressEvent(self, event):
        # Позиция относительно self.map_render
        pos = self.map_render.mapFromParent(event.pos())
        pos = (pos.x(), pos.y())

        if 0 <= pos[0] <= 600 and 0 <= pos[1] <= 450:
            if event.button() == Qt.LeftButton:
                # Левая конпки мыши
                self.find_object_by_click(pos)
            elif event.button() == Qt.RightButton:
                # Правая конпки мыши
                self.find_organisation(pos)

    # Найти организацию
    def find_organisation(self, pos):
        coord = tuple(map(float, self.static_api_handler.params['ll'].split(',')))
        spn = tuple(map(float, self.static_api_handler.params['spn'].split(',')))

        pos_new = self.get_points_from_pos(pos, spn, coord)
        self.geocoder_api_handler.set_params(key=('geocode', pos_new))
        self.search_api_handler.new_response(pos=tuple(map(float, pos_new.split(','))))
        if self.search_api_handler.object_found:
            self.set_new_object(self.search_api_handler.get_point())
            self.find_object(responsed=True)
        else:
            self.address_text.setPlainText('Организация не найдена')

    # Найти объект по клику
    def find_object_by_click(self, pos):
        # Координаты центра карты
        coord = tuple(map(float, self.static_api_handler.params['ll'].split(',')))
        # Охват карты
        spn = tuple(map(float, self.static_api_handler.params['spn'].split(',')))
        points = self.get_points_from_pos(pos, spn, coord)
        self.find_object(points)

    # Получим долготу и широту на которую кликнули
    def get_points_from_pos(self, pos, spn, coord):
        # Преобразуем pos в pos относительно центра map_render
        pos = tuple((pos[i] - self.MAP_RENDER_SIZE[i] // 2) * (1, -1)[i]
                    for i in range(2))
        # Рассчитаем на какие координаты по клику мы попали
        # Преобразуем spn в долготу/широту за единицу на координатах
        spn = tuple(spn[i] / self.MAP_RENDER_SIZE[i] for i in range(2))
        # Разница координат
        spn = tuple(pos[i] * spn[i] for i in range(2))
        # Возвращаем координаты по которым кликнули
        return ','.join(tuple(str(round(coord[i] + spn[i], 6)) for i in range(2)))

    # Событие нажития клавиши
    def keyPressEvent(self, event):
        key = event.key()
        print(key)
        new_response = False
        delta = float(self.static_api_handler.params['spn'].split(',')[0])
        delta_posx = {Qt.Key_Right: delta, Qt.Key_Left: -delta}
        delta_posy = {Qt.Key_Up: delta, Qt.Key_Down: -delta}
        if key == Qt.Key_PageDown or key == Qt.Key_PageUp:
            key = -0.002 if key == Qt.Key_PageUp else 0.002
            if 0.006 <= delta + key <= 2:
                new_response = True
                self.static_api_handler.set_params(key=('spn', ','.join(str(delta + key) for _ in range(2))))
        elif key in delta_posx.keys() or key in delta_posy:
            delta_x = delta_y = 0
            if key in delta_posx.keys():
                delta_x = delta_posx[key]
            else:
                delta_y = delta_posy[key]
            pos = list(map(float, self.static_api_handler.params['ll'].split(',')))
            if abs(pos[0] + delta_x) > 180:
                pos[0] = 180 * (delta_x // abs(delta_x))
            else:
                pos[0] += delta_x
            if abs(pos[1] + delta_y) > 90:
                pos[1] = 90 * (delta_y // abs(delta_y))
            else:
                pos[1] += delta_y
            self.static_api_handler.set_params(key=('ll', ','.join(map(str, pos))))
            new_response = True

        if new_response:
            self.new_img()
