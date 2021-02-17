import sys
from PyQt5.QtWidgets import QApplication
from source.scripts.MainWindow import MainWindow
from source.scripts.ApiHandler import ApiHandler
from source.scripts.CacheHandler import CacheHandler
import source.scripts.config as config


if __name__ == '__main__':
    # Api Handler
    url, params = config.url, config.params
    handler = ApiHandler(url, params, CacheHandler('cache/'))  # cache/ - место кеширования
    app = QApplication(sys.argv)
    window = MainWindow(handler.get_map(), handler.get_status())
    window.show()
    sys.exit(app.exec_())
