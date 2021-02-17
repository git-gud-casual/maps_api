# maps_api
Yandex.Lyceum

CacheHandler - просматривает есть ли в папке картинка по подключению с определенными параметрами и если нет сохраняет. Работает в связке с ApiHandler. 
Работая с классом ApiHandler, удобнее пользоваться методом set_params(), все остальное класс сделает сам. То есть, для показа нескольких картинок достаточно изменить параметры
с помощью ApiHandler.set_params(params), а далее отобразить картинку с помощью MainWindow.new_img(ApiHandler.get_map(), ApiHandler.get_status())
