from logic.services import (
    view_in_wishlist,
    add_to_wishlist,
    remove_from_wishlist,
)
from django.http import JsonResponse, HttpResponseNotFound
from store.models import DATABASE
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required


JSON_PARAMS: dict = {"ensure_ascii": False, "indent": 4}

ERROR_NOT_IN_DATABASE: str = "Данного продукта нет в базе данных"
ERROR_WISHLIST_ADD: str = "Неудачное добавление в избранное"
ERROR_WISHLIST_REMOVE: str = "Неудачное удаление из избранного"
ERROR_DATA: str = "Неверные данные"
ERROR_AUTH: str = "Пользователь не авторизован"

SUCCESS_WISHLIST_ADD: str = "Продукт успешно добавлен в избранное"
SUCCESS_WISHLIST_REMOVE: str = "Продукт успешно удален из избранного"


@login_required(login_url="login:login_view")
def wishlist_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist(request)[current_user]

        products = []
        for product_id in data["products"]:
            product = DATABASE.get(product_id)
            product["price_total"] = f"{product['price_after']:.2f}"
            products.append(product)

        return render(request, "wishlist/wishlist.html", context={"products": products})


@login_required(login_url="login:login_view")
def wishlist_add_view(request, id_product: str):
    if request.method == "GET":
        result = add_to_wishlist(request, id_product)

        if result:
            return JsonResponse(
                {"answer": SUCCESS_WISHLIST_ADD},
                json_dumps_params=JSON_PARAMS,
            )

        return JsonResponse(
            {"answer": ERROR_WISHLIST_ADD},
            status=404,
            json_dumps_params=JSON_PARAMS,
        )


@login_required(login_url="login:login_view")
def wishlist_del_view(request, id_product: str):
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)

        if result:
            return JsonResponse(
                {"answer": SUCCESS_WISHLIST_REMOVE},
                json_dumps_params=JSON_PARAMS,
            )

        return JsonResponse(
            {"answer": ERROR_WISHLIST_REMOVE},
            status=404,
            json_dumps_params=JSON_PARAMS,
        )


@login_required(login_url="login:login_view")
def wishlist_json(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_wishlist(request)[current_user]

        if data:
            return JsonResponse(data, json_dumps_params=JSON_PARAMS)

        return JsonResponse(
            {"answer": ERROR_AUTH}, status=404, json_dumps_params=JSON_PARAMS
        )


def wishlist_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_wishlist(request, id_product)

        if result:
            return redirect("wishlist:wishlist")

        return HttpResponseNotFound(ERROR_WISHLIST_REMOVE)
