from django.http import JsonResponse
import requests
from datetime import datetime


DIRECTION_TRANSFORM = {
    "n": "северное",
    "nne": "северо - северо - восточное",
    "ne": "северо - восточное",
    "ene": "восточно - северо - восточное",
    "e": "восточное",
    "ese": "восточно - юго - восточное",
    "se": "юго - восточное",
    "sse": "юго - юго - восточное",
    "s": "южное",
    "ssw": "юго - юго - западное",
    "sw": "юго - западное",
    "wsw": "западно - юго - западное",
    "w": "западное",
    "wnw": "западно - северо - западное",
    "nw": "северо - западное",
    "nnw": "северо - северо - западное",
    "c": "штиль",
}


def current_weather(lat, lon):
    token = "2048d6fe-9ec3-4660-b1b4-ea76e9d417dc"
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"
    headers = {"X-Yandex-API-Key": f"{token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    result = {
        "city": data["geo_object"]["locality"]["name"],
        "time": datetime.fromtimestamp(data["fact"]["uptime"]).strftime("%H:%M"),
        "temp": data["fact"]["temp"],
        "feels_like_temp": data["fact"]["feels_like"],
        "pressure": data["fact"]["pressure_mm"],
        "humidity": data["fact"]["humidity"],
        "wind_speed": data["fact"]["wind_speed"],
        "wind_gust": data["fact"]["wind_gust"],
        "wind_dir": DIRECTION_TRANSFORM.get(data["fact"]["wind_dir"]),
    }
    return result


def weather_view(request):
    if request.method == "GET":
        lat = request.GET.get("lat")
        lon = request.GET.get("lon")
        if lat and lon:
            data = current_weather(lat=lat, lon=lon)
        else:
            data = current_weather(59.93, 30.31)
        return JsonResponse(
            data, json_dumps_params={"ensure_ascii": False, "indent": 4}
        )
