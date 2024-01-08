from logic.services import (
    view_in_wishlist,
    add_to_wishlist,
    remove_from_wishlist,
    add_user_to_wishlist,
)
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from store.models import DATABASE
from logic.services import filtering_category
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required


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


def wishlist_add_json(request, id_product: str):
    ...


def wishlist_del_json(request, id_product: str):
    ...


def wishlist_json(request):
    ...
