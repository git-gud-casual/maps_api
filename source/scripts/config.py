# Здесь находятся параметры и url, ибо их необходимо задавать программно
url = "http://static-maps.yandex.ru/1.x/"

lon = "37.530887"
lat = "55.703118"
delta = "0.003"
l_param = "map"

params = {
    "ll": ",".join([lon, lat]),
    "spn": ",".join([delta, delta]),
    "l": l_param
}
