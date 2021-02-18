# Здесь находятся параметры и url, ибо их необходимо задавать программно
# static_api данные
static_api_url = "http://static-maps.yandex.ru/1.x/"

lon = "37.530887"
lat = "55.703118"
delta = "0.003"
l_param = "map"

static_api_params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": l_param,
    "pt": None
}

# Поиск по организациям API данные
search_api_key = ''  # Вставить ключ от API для поиска по организациям
search_api_url = 'https://search-maps.yandex.ru/v1/'

search_api_params = {
    'apikey': search_api_key,
    'text': None,
    'lang': 'ru_RU',
    'spn': static_api_params['spn'],
    'll': static_api_params['ll']
}
