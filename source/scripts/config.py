# Здесь находятся параметры и url, ибо их необходимо задавать программно
# static_api данные
static_api_url = "http://static-maps.yandex.ru/1.x/"

lon = "37.530887"
lat = "55.703118"
delta = "0.01"
l_param = "map"

static_api_params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": l_param,
    "pt": None
}

# Поиск по организациям API данные
search_api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'  # Вставить ключ от API для поиска по организациям
search_api_url = 'https://search-maps.yandex.ru/v1/'

search_api_params = {
    'apikey': search_api_key,
    'text': None,
    'lang': 'ru_RU',
    'type': 'biz'
}

# GeoCoder API данные
geocoder_api_key = '40d1649f-0493-4b70-98ba-98533de7710b'  # Вставить ключ
geocoder_api_url = 'https://geocode-maps.yandex.ru/1.x'

geocoder_api_params = {
    'geocode': None,
    'apikey': geocoder_api_key,
    'format': 'json'
}
