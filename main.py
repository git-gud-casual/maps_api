import sys
from PyQt5.QtWidgets import QApplication
from source.scripts.MainWindow import MainWindow
from source.scripts.StaticApiHandler import StaticApiHandler
from source.scripts.SearchApiHandler import SearchApiHandler
from source.scripts.CacheHandler import CacheHandler
import source.scripts.config as config


if __name__ == '__main__':
    # StaticApiHandler
    static_api_handler = StaticApiHandler(config.static_api_url,
                                          config.static_api_params, CacheHandler('cache/'))
    # SearchApiHandler
    search_api_handler = SearchApiHandler(config.search_api_url, config.search_api_params)

    app = QApplication(sys.argv)
    window = MainWindow(static_api_handler, search_api_handler)
    window.show()
    sys.exit(app.exec_())
