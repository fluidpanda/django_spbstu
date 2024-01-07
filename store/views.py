from django.shortcuts import render
from logic.services import view_in_cart, add_to_cart, remove_from_cart
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from .models import DATABASE
from logic.services import filtering_category
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required


JSON_PARAMS: dict = {"ensure_ascii": False, "indent": 4}

DATA_COUPON: dict = {
    "coupon": {"value": 10, "is_valid": True},
    "coupon_old": {"value": 20, "is_valid": False},
}

DATA_PRICE: dict = {
    "Россия": {
        "Москва": {"price": 80},
        "Санкт-Петербург": {"price": 80},
        "fix_price": 100,
    },
}

ERROR_NOT_IN_DATABASE: str = "Данного продукта нет в базе данных"
ERROR_CART_ADD: str = "Неудачное добавление в корзину"
ERROR_CART_REMOVE: str = "Неудачное удаление из корзины"
ERROR_COUPON: str = "Неверный купон"
ERROR_DATA: str = "Неверные данные"

SUCCESS_CART_ADD: str = "Продукт успешно добавлен в корзину"
SUCCESS_CART_REMOVE: str = "Продукт успешно удален из корзины"


def products_view(request):
    if request.method == "GET":
        if id_product := request.GET.get("id"):
            if data := DATABASE.get(id_product):
                return JsonResponse(data, json_dumps_params=JSON_PARAMS)
            return HttpResponseNotFound(ERROR_NOT_IN_DATABASE)

        category_key = request.GET.get("category")
        if ordering_key := request.GET.get("ordering"):
            if request.GET.get("reverse") in (
                "true",
                "True",
            ):
                data = filtering_category(
                    DATABASE, category_key, ordering_key, reverse=True
                )
            else:
                data = filtering_category(
                    DATABASE, category_key, ordering_key, reverse=False
                )
        else:
            data = filtering_category(DATABASE, category_key)

        return JsonResponse(data, safe=False, json_dumps_params=JSON_PARAMS)


def products_page_view(request, page):
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
                    f'store/products/{data["html"]}.html', encoding="utf-8"
                ) as file:
                    data = file.read()

                return HttpResponse(data)

        return HttpResponse(status=404)


def shop_view(request):
    if request.method == "GET":
        return render(
            request, "store/shop.html", context={"products": DATABASE.values()}
        )


@login_required(login_url="login:login_view")
def cart_view(request):
    if request.method == "GET":
        current_user = get_user(request).username
        data = view_in_cart(request)[current_user]
        if request.GET.get("format") == "JSON":
            return JsonResponse(data, json_dumps_params=JSON_PARAMS)

        products = []
        for product_id, quantity in data["products"].items():
            product = DATABASE[product_id]
            product["quantity"] = quantity
            product["price_total"] = f"{quantity * product['price_after']:.2f}"
            products.append(product)
        return render(request, "store/cart.html", context={"products": products})


@login_required(login_url="login:login_view")
def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(request, id_product)
        if result:
            return JsonResponse(
                {"answer": SUCCESS_CART_ADD},
                json_dumps_params=JSON_PARAMS,
            )
        return JsonResponse(
            {"answer": ERROR_CART_ADD},
            status=404,
            json_dumps_params=JSON_PARAMS,
        )


def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(request, id_product)
        if result:
            return JsonResponse(
                {"answer": SUCCESS_CART_REMOVE},
                json_dumps_params=JSON_PARAMS,
            )

        return JsonResponse(
            {"answer": ERROR_CART_REMOVE},
            status=404,
            json_dumps_params=JSON_PARAMS,
        )


def coupon_check_view(request, name_coupon):
    if request.method == "GET":
        if name_coupon in DATA_COUPON.keys():
            return JsonResponse(
                {
                    "discount": DATA_COUPON["coupon"]["value"],
                    "is_valid": DATA_COUPON["coupon"]["is_valid"],
                }
            )

        return HttpResponseNotFound(ERROR_COUPON)


def delivery_estimate_view(request):
    if request.method == "GET":
        data = request.GET
        country = data.get("country")
        city = data.get("city")

        if country in DATA_PRICE.keys():
            if city in DATA_PRICE[country].keys():
                return JsonResponse({"price": DATA_PRICE[country][city]["price"]})
            else:
                return JsonResponse({"price": DATA_PRICE[country]["fix_price"]})

        return HttpResponseNotFound(ERROR_DATA)


@login_required(login_url="login:login_view")
def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(request, id_product)
        if result:
            return redirect("store:cart_view")

        return HttpResponseNotFound(ERROR_CART_ADD)


def cart_remove_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(request, id_product)
        if result:
            return redirect("store:cart_view")

        return HttpResponseNotFound(ERROR_CART_REMOVE)
