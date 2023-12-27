from .models import DATABASE
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from logic.services import (
    filtering_category,
    view_in_cart,
    add_to_cart,
    remove_from_cart,
)
from django.shortcuts import render

JSON_PARAMS: dict = {"ensure_ascii": False, "indent": 4}
NOT_IN_DATABASE: str = "Данного продукта нет в базе данных"


def products_view(request):
    if request.method == "GET":
        id_param: str = request.GET.get("id")

        if id_param and id_param not in DATABASE:
            return HttpResponseNotFound(NOT_IN_DATABASE)
        elif id_param and id_param in DATABASE:
            return JsonResponse(
                DATABASE.get(str(id_param)),
                json_dumps_params=JSON_PARAMS,
            )
        else:
            return JsonResponse(DATABASE, json_dumps_params=JSON_PARAMS)

        if id_product := request.GET.get("id"):
            if data := DATABASE.get(id_product):
                return JsonResponse(data, json_dumps_params=JSON_PARAMS)
            return HttpResponseNotFound(NOT_IN_DATABASE)

        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse") in ("true", "True"):
                data = ...
            else:
                data = ...
        else:
            data = ...
        return JsonResponse(data, safe=False, json_dumps_params=JSON_PARAMS)


def product_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data["html"] == page:
                    with open(f"store/products/{page}.html", encoding="utf-8") as file:
                        data = file.read()
                        return HttpResponse(data)
        elif isinstance(page, int):
            data = DATABASE.get(str(page))
            if data:
                with open(
                    f"store/products/{data['html']}.html", encoding="utf-8"
                ) as file:
                    data = file.read()
                    return HttpResponse(data)

        return HttpResponse(status=404)


def shop_view(request):
    if request.method == "GET":
        return render(
            request, "store/shop.html", context={"products": DATABASE.values()}
        )


def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()
        if request.GET.get("format") == "JSON":
            return JsonResponse(data, json_dumps_params=JSON_PARAMS)

        products = []
        for product_id, quantity in data["products"].items():
            product = DATABASE.get(product_id)
            product["quantity"] = quantity
            product["price_total"] = f"{quantity * product['price_after']:.2f}"
            products.append(product)

        return render(request, "store/cart.html", context={"products": products})


def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product)
        if result:
            return JsonResponse(
                {"answer": "Продукт успешно добавлен в корзину"},
                json_dumps_params=JSON_PARAMS,
            )


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product)
        if result:
            return JsonResponse(
                {"answer": "Продукт успешно удален из корзины"},
                json_dumps_params=JSON_PARAMS,
            )

        return JsonResponse(
            {"answer": "Неудачное удаление из корзины"}, json_dumps_params=JSON_PARAMS
        )
