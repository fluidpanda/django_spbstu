from .models import DATABASE
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound


def products_view(request):
    if request.method == "GET":
        id_param: str = request.GET.get("id")
        if id_param and id_param not in DATABASE:
            return HttpResponseNotFound("Данного продукта нет в базе данных")
        if id_param and id_param in DATABASE:
            return JsonResponse(
                DATABASE.get(str(id_param)),
                json_dumps_params={"ensure_ascii": False, "indent": 4},
            )
        else:
            return JsonResponse(
                DATABASE, json_dumps_params={"ensure_ascii": False, "indent": 4}
            )


def shop_view(request):
    if request.method == "GET":
        with open("store/shop.html", encoding="utf-8") as file:
            data = file.read()
            return HttpResponse(data)
